"""Load a trained tiny GPT checkpoint and generate text.

Example usage:
    python sample.py --ckpt checkpoints/tinygpt_shakespeare.pt --start "ROMEO: "
"""

from __future__ import annotations

import argparse

import torch

from model import GPTConfig, TinyGPT


def encode(text: str, stoi: dict[str, int]) -> list[int]:
    return [stoi[ch] for ch in text]


def decode(tokens: list[int], itos: dict[int, str]) -> str:
    return "".join(itos[i] for i in tokens)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample text from tiny GPT checkpoint")
    parser.add_argument("--ckpt", type=str, default="checkpoints/tinygpt_shakespeare.pt")
    parser.add_argument("--start", type=str, default="To be")
    parser.add_argument("--max_new_tokens", type=int, default=400)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    checkpoint = torch.load(args.ckpt, map_location=args.device)

    cfg = GPTConfig(**checkpoint["model_config"])
    model = TinyGPT(cfg).to(args.device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    stoi = checkpoint["stoi"]
    itos = {int(k): v for k, v in checkpoint["itos"].items()}

    # If user gave chars not in vocab, replace with space when possible.
    if " " in stoi:
        safe_start = "".join(ch if ch in stoi else " " for ch in args.start)
    else:
        safe_start = "".join(ch for ch in args.start if ch in stoi)

    if not safe_start:
        safe_start = "\n"

    start_tokens = torch.tensor([encode(safe_start, stoi)], dtype=torch.long, device=args.device)

    with torch.no_grad():
        out_tokens = model.generate(start_tokens, max_new_tokens=args.max_new_tokens)[0].tolist()

    print("=== GENERATED TEXT ===")
    print(decode(out_tokens, itos))


if __name__ == "__main__":
    main()
