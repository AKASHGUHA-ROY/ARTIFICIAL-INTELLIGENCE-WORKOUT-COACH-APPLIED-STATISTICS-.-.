# Phase 2 Report

## Objective
For Phase 2, we implemented a small GPT-style language model in PyTorch and trained it on a text dataset using a character-level approach. Our goal was to understand how a nanoGPT-style transformer works, how different architecture choices affect training behavior, and how generated text quality changes across multiple experimental configurations. This phase serves as a technical foundation for our later MVP, where language-model ideas may support natural-language workout guidance and coaching-style feedback.

## Model Architecture
Our model is a small transformer-based character language model. The architecture includes:
- a token embedding layer that maps each character ID to a dense vector
- a positional embedding layer that helps the model understand token order
- masked self-attention so each position can only attend to previous positions
- a feedforward network inside each transformer block
- residual connections and layer normalization for stable training
- a final linear output head that predicts the next character

The model is implemented in `model.py` and is intentionally small enough to run on a normal laptop for educational experimentation.

## Training Setup
We used the Tiny Shakespeare dataset as our baseline text corpus. The model uses **character-level tokenization**, meaning each unique character is treated as a vocabulary item and mapped to an integer ID. The dataset is split into training and validation sets using a 90/10 split.

Our training script is implemented in `train.py`. It:
- loads the dataset
- builds the character vocabulary
- encodes the text into integer IDs
- samples training batches
- trains the model with AdamW
- evaluates train and validation loss during training
- saves a checkpoint for later text generation

Initial default setup:
- Dataset: Tiny Shakespeare
- Tokenization: Character-level
- Train/validation split: 90/10
- Optimizer: AdamW
- Learning rate: 3e-4
- Batch size: 32
- Baseline context length: 128
- Baseline embedding dimension: 128
- Baseline attention heads: 4
- Baseline transformer layers: 4

## Experiments
The course guideline requires at least three experimental configurations varying architecture choices such as layers, heads, embedding dimension, context length, or dropout. 

We used the following three configurations:

| Config | Layers | Heads | Embedding Dim | Context Length | Dropout | Notes |
|---|---:|---:|---:|---:|---:|---|
| Small | 2 | 2 | 64 | 64 | 0.1 | Small baseline model |
| Medium | 4 | 4 | 128 | 64 | 0.1 | Larger model capacity |
| Context | 4 | 4 | 128 | 128 | 0.2 | Longer context and more regularization |

### Results Table
Fill this in after training:

| Config | Params | Training Time | Best Validation Loss | Final Validation Loss |
|---|---:|---:|---:|---:|
| Small | TBD | TBD | TBD | TBD |
| Medium | TBD | TBD | TBD | TBD |
| Context | TBD | TBD | TBD | TBD |

### Loss Curves
We will include training and validation loss curves in the `plots/` folder as required by the project guideline. :contentReference[oaicite:2]{index=2}

Expected files:
- `plots/loss_small.png`
- `plots/loss_medium.png`
- `plots/loss_context.png`

## Qualitative Samples
The project guideline asks for generated text samples for at least two configurations. :contentReference[oaicite:3]{index=3}

We will generate sample text using `sample.py` after training.

### Sample Output — Small
```text
TBD
TBD

