"""Train a tiny GPT-style character model on Tiny Shakespeare.

Example usage:
    python train.py
    python train.py --data_path docs/nanogpt/data/tiny_shakespeare.txt
"""

from __future__ import annotations

import argparse
import os
import random
import urllib.request
from dataclasses import asdict

import torch

from model import GPTConfig, TinyGPT


TINY_SHAKESPEARE_URL = (
    "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
)


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def maybe_download_tiny_shakespeare(path: str) -> None:
    if os.path.isfile(path):
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"Dataset not found at {path}. Downloading Tiny Shakespeare...")
    urllib.request.urlretrieve(TINY_SHAKESPEARE_URL, path)
    print(f"Downloaded Tiny Shakespeare to: {path}")


def load_text(path: str) -> str:
    if os.path.isfile(path):
        chosen = path
    else:
        script_relative = os.path.join(os.path.dirname(__file__), path)
        if os.path.isfile(script_relative):
            chosen = script_relative
        else:
            raise FileNotFoundError(f"Could not find dataset at: {path}")

    with open(chosen, "r", encoding="utf-8") as f:
        return f.read()


def build_vocab(text: str):
    chars = sorted(list(set(text)))
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for ch, i in stoi.items()}
    return chars, stoi, itos


def encode(text: str, stoi: dict[str, int]) -> list[int]:
    return [stoi[ch] for ch in text]


def decode(tokens: list[int], itos: dict[int, str]) -> str:
    return "".join(itos[i] for i in tokens)


def get_batch(data: torch.Tensor, block_size: int, batch_size: int, device: str):
    starts = torch.randint(0, len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[s : s + block_size] for s in starts])
    y = torch.stack([data[s + 1 : s + block_size + 1] for s in starts])
    return x.to(device), y.to(device)


@torch.no_grad()
def estimate_loss(model: TinyGPT, train_data: torch.Tensor, val_data: torch.Tensor, cfg):
    model.eval()
    out = {}
    for split, split_data in [("train", train_data), ("val", val_data)]:
        losses = torch.zeros(cfg.eval_iters)
        for k in range(cfg.eval_iters):
            xb, yb = get_batch(split_data, cfg.block_size, cfg.batch_size, cfg.device)
            _, loss = model(xb, yb)
            losses[k] = loss.item()
        out[split] = losses.mean().item()
    model.train()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Train tiny GPT on Tiny Shakespeare")
    parser.add_argument("--data_path", type=str, default="docs/nanogpt/data/tiny_shakespeare.txt")
    parser.add_argument("--out_dir", type=str, default="checkpoints")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--block_size", type=int, default=128)
    parser.add_argument("--n_embd", type=int, default=128)
    parser.add_argument("--n_head", type=int, default=4)
    parser.add_argument("--n_layer", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--learning_rate", type=float, default=3e-4)
    parser.add_argument("--max_iters", type=int, default=2000)
    parser.add_argument("--eval_interval", type=int, default=200)
    parser.add_argument("--eval_iters", type=int, default=100)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    set_seed(args.seed)
    os.makedirs(args.out_dir, exist_ok=True)
    maybe_download_tiny_shakespeare(args.data_path)

    print(f"Loading data from: {args.data_path}")
    text = load_text(args.data_path)
    chars, stoi, itos = build_vocab(text)
    vocab_size = len(chars)
    print(f"Dataset length: {len(text):,} characters")
    print(f"Vocab size: {vocab_size}")

    if len(text) < args.block_size + 2:
        raise ValueError(
            f"Dataset is too short ({len(text)} chars) for block_size={args.block_size}. "
            "Use a larger dataset or lower --block_size."
        )

    data = torch.tensor(encode(text, stoi), dtype=torch.long)
    n = int(0.9 * len(data))
    train_data = data[:n]
    val_data = data[n:]

    model_cfg = GPTConfig(
        vocab_size=vocab_size,
        block_size=args.block_size,
        n_embd=args.n_embd,
        n_head=args.n_head,
        n_layer=args.n_layer,
        dropout=args.dropout,
    )

    model = TinyGPT(model_cfg).to(args.device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)

    class EvalCfg:
        eval_iters = args.eval_iters
        block_size = args.block_size
        batch_size = args.batch_size
        device = args.device

    print("Starting training.")
    for step in range(args.max_iters + 1):
        if step % args.eval_interval == 0:
            losses = estimate_loss(model, train_data, val_data, EvalCfg)
            print(
                f"step {step:4d} | train loss {losses['train']:.4f} | "
                f"val loss {losses['val']:.4f}"
            )

        xb, yb = get_batch(train_data, args.block_size, args.batch_size, args.device)
        _, loss = model(xb, yb)

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    ckpt_path = os.path.join(args.out_dir, "tinygpt_shakespeare.pt")
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "model_config": asdict(model_cfg),
        "stoi": stoi,
        "itos": itos,
        "train_args": vars(args),
    }
    torch.save(checkpoint, ckpt_path)
    print(f"Saved checkpoint to: {ckpt_path}")

    model.eval()
    start = torch.zeros((1, 1), dtype=torch.long, device=args.device)
    sampled_tokens = model.generate(start, max_new_tokens=300)[0].tolist()
    print("\n=== SAMPLE ===")
    print(decode(sampled_tokens, itos))


if __name__ == "__main__":
    main()
     