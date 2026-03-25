"""A tiny, beginner-friendly GPT-style character model in PyTorch.

This file intentionally keeps things small and explicit so it is easy to read.
The architecture includes:
- token embeddings
- positional embeddings
- masked self-attention (causal attention)
- feedforward network (MLP)
- transformer blocks + residual connections
- layer normalization
- final linear language-model head
"""

from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class GPTConfig:
    """Configuration for a very small GPT model."""

    vocab_size: int
    block_size: int = 128  # context length (how many chars model can look back)
    n_embd: int = 128  # embedding size
    n_head: int = 4  # number of attention heads
    n_layer: int = 4  # number of transformer blocks
    dropout: float = 0.1


class CausalSelfAttention(nn.Module):
    """Multi-head masked self-attention.

    "Masked" (causal) means token t can only attend to tokens <= t,
    never to the future.
    """

    def __init__(self, config: GPTConfig):
        super().__init__()
        assert config.n_embd % config.n_head == 0, "n_embd must be divisible by n_head"

        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.head_dim = config.n_embd // config.n_head

        # Single projection for query, key, value (then split into 3 chunks).
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        # Output projection after concatenating heads.
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)

        # Precompute a lower-triangular mask for causal attention.
        # Shape: (1, 1, T, T) so it can broadcast over batch and heads.
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(config.block_size, config.block_size)).view(
                1, 1, config.block_size, config.block_size
            ),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        bsz, t, c = x.size()  # batch, time, channels

        # Project once, then split into q, k, v.
        qkv = self.c_attn(x)  # (B, T, 3C)
        q, k, v = qkv.split(self.n_embd, dim=2)

        # Reshape into heads: (B, nh, T, hs)
        q = q.view(bsz, t, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(bsz, t, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(bsz, t, self.n_head, self.head_dim).transpose(1, 2)

        # Attention scores: (B, nh, T, T)
        att = (q @ k.transpose(-2, -1)) * (1.0 / (self.head_dim**0.5))

        # Apply causal mask: block future positions.
        att = att.masked_fill(self.bias[:, :, :t, :t] == 0, float("-inf"))

        # Convert scores to probabilities.
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)

        # Weighted sum of values.
        y = att @ v  # (B, nh, T, hs)

        # Reassemble all heads: (B, T, C)
        y = y.transpose(1, 2).contiguous().view(bsz, t, c)

        # Final projection + dropout.
        y = self.resid_dropout(self.c_proj(y))
        return y


class FeedForward(nn.Module):
    """Simple 2-layer MLP used inside each transformer block."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.GELU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class Block(nn.Module):
    """Transformer block: LayerNorm -> Attention -> residual, then LayerNorm -> MLP -> residual."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = FeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class TinyGPT(nn.Module):
    """A tiny GPT-style character language model."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.config = config

        # Embedding tables.
        self.token_embedding = nn.Embedding(config.vocab_size, config.n_embd)
        self.position_embedding = nn.Embedding(config.block_size, config.n_embd)

        self.drop = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList([Block(config) for _ in range(config.n_layer)])
        self.ln_f = nn.LayerNorm(config.n_embd)

        # Final linear layer to predict next character logits.
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
        """Initialize model parameters with small random values."""
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None):
        """Forward pass.

        Args:
            idx: token indices, shape (B, T)
            targets: optional target indices, shape (B, T)

        Returns:
            logits: shape (B, T, vocab_size)
            loss: cross-entropy loss if targets provided, else None
        """
        bsz, t = idx.size()
        if t > self.config.block_size:
            raise ValueError(f"Cannot forward sequence of length {t}, block size is {self.config.block_size}")

        # Build positions [0..T-1].
        pos = torch.arange(0, t, device=idx.device)

        # Token + positional embeddings.
        tok_emb = self.token_embedding(idx)  # (B, T, C)
        pos_emb = self.position_embedding(pos)  # (T, C)
        x = self.drop(tok_emb + pos_emb)

        # Pass through transformer blocks.
        for block in self.blocks:
            x = block(x)

        x = self.ln_f(x)
        logits = self.lm_head(x)

        loss = None
        if targets is not None:
            # Flatten batch and time for cross entropy.
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))

        return logits, loss

    @torch.no_grad()
    def generate(self, idx: torch.Tensor, max_new_tokens: int) -> torch.Tensor:
        """Autoregressive text generation.

        Repeatedly predicts the next token and appends it to the sequence.
        """
        for _ in range(max_new_tokens):
            # Crop to model context window.
            idx_cond = idx[:, -self.config.block_size :]
            logits, _ = self(idx_cond)

            # Use logits at the last time step.
            logits = logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)

            # Sample next token from probability distribution.
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx
