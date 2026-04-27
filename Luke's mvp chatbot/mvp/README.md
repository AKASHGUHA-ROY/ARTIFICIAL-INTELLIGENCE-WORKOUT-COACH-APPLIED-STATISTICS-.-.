# MVP Workout Planner

This folder contains a small rule-based MVP for an AI workout assistant.

It uses:

- a local JSON exercise dataset
- simple Python selection rules
- no external APIs
- no model training

## Run the benchmark demo

From the repository root, run the fixed benchmark-style cases:

```bash
python3 src/demo.py
```

## Run the interactive demo

To type in your own workout preferences:

```bash
python3 src/chat_demo.py
```

The interactive demo asks for experience level, workout focus, minutes available, equipment, whether the user needs dorm-friendly options, and an optional pain area.

## Demo cases

The benchmark demo currently includes 5 cases:

- beginner arm day, no equipment, 20 minutes
- intermediate back day, dumbbells only, 45 minutes
- beginner leg day with knee pain
- busy student full-body workout, 15 minutes
- user reports high effort and pain after a set

## What the planner does

The planner:

- filters exercises by level, equipment, time, and pain constraints
- keeps pain-related plans conservative
- builds balanced full-body sessions across upper body, lower body, and core/cardio
- limits exact exercise repetition so plans feel less repetitive
- returns a short rationale for each plan

## Data notes

The local dataset was expanded with a small filtered subset inspired by public exercise data sources, including [wrkout/exercises.json](https://github.com/wrkout/exercises.json) and the [wger exercise database](https://github.com/wger-project/wger). The added exercises were normalized into this project's existing beginner-friendly schema. No external API is called at runtime, and no large dataset import, media, or detailed source instructions were copied into the MVP.

## Project files

- `data/exercises.json`: beginner-friendly exercise dataset
- `src/planner.py`: rule-based workout planner and selection logic
- `src/demo.py`: runs the 5 benchmark-style sample cases
- `src/chat_demo.py`: asks for user input in the terminal and prints a custom plan
- `artifacts/improved_outputs.md`: saved benchmark outputs for the current MVP
- `report.md`: short class-project MVP report
