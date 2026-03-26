# Phase 2 - nanoGPT

## Overview
This folder contains our Phase 2 nanoGPT project for MAE301.  
We implemented a small GPT-style character-level language model in PyTorch and trained it on the Tiny Shakespeare dataset.

## Files
- `model.py` - defines the tiny GPT-style model
- `train.py` - trains the model on a text dataset
- `sample.py` - loads a trained checkpoint and generates text
- `requirements.txt` - Python packages needed
- `configs/` - experiment configurations
- `data/` - dataset files
- `plots/` - loss curves and result plots
- `report.md` - Phase 2 report

## Setup
Install dependencies with:

```bash
pip install -r requirements.txt
