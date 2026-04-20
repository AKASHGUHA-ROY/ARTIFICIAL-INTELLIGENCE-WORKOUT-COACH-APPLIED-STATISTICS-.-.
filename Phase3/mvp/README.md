# MVP Workout Planner

This folder contains a small rule-based MVP for an AI workout assistant.

It uses:

- a local JSON exercise dataset
- simple Python selection rules
- no external APIs
- no model training

## Files

- `data/exercises.json`: beginner-friendly exercise dataset
- `src/planner.py`: rule-based workout planner
- `src/demo.py`: runs the 5 benchmark-style sample cases

## Run the demo

From the repository root:

```bash
python3 mvp/src/demo.py
```

## What the planner does

The planner:

- filters exercises by level, equipment, time, and pain constraints
- keeps pain-related plans conservative
- builds balanced full-body sessions across upper body, lower body, and core/cardio
- limits exact exercise repetition so plans feel less repetitive
- returns a short rationale for each plan

## Sample cases

The demo covers:

- beginner arm day, no equipment, 20 minutes
- intermediate back day, dumbbells only, 45 minutes
- beginner leg day with knee pain
- busy student full-body workout, 15 minutes
- user reports high effort and pain after a set
