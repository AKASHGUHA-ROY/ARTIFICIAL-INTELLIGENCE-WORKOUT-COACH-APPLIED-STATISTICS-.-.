# Luke Payne MVP Version

## Project Title

AI Workout Assistant MVP

## What this MVP does

This MVP is a small workout assistant for busy students and beginner lifters. The user enters workout focus, available equipment, time, experience level, dorm-friendly needs, pain status, and effort level. The app returns a simple workout plan with exercise choices, estimated time, sets and reps style guidance, rest suggestions, form cues, rationale, and safety notes.

This version is intentionally transparent. It uses a local exercise dataset and rule-based planning logic instead of a trained model or outside API. That makes the project easier to run, explain, and evaluate for MAE 301.

## Folder Structure

```text
Luke Payne MVP version/
├── README.md
├── report.md
├── requirements.txt
├── app.py
├── data/
│   └── exercises.json
├── src/
│   ├── __init__.py
│   ├── planner.py
│   └── demo.py
└── artifacts/
    ├── demo_outputs.md
    └── streamlit_screenshot_evidence.pdf
```

## Setup

From inside this folder, install the required package.

```bash
pip install -r requirements.txt
```

## Run the Web App

From inside this folder, run:

```bash
streamlit run app.py
```

The app opens a Streamlit interface where the user can enter workout constraints and receive a plan.

## Run the Command-Line Demo

From inside this folder, run:

```bash
python src/demo.py
```

This runs benchmark-style test cases and rewrites:

```text
artifacts/demo_outputs.md
```

## Required Data

The MVP uses:

```text
data/exercises.json
```

The dataset has 31 exercise entries. Each entry includes exercise name, body part, equipment, experience level, estimated time, role, dorm-friendly status, pain flags, and tags.

## No API Keys Required

This project does not require API keys, paid models, or internet access once the files are downloaded.

## What Improved in This Version

- Cleaned the MVP into one folder.
- Added stronger setup and demo instructions.
- Added sets and reps style workout guidance.
- Added rest time and form cues for each exercise.
- Added clearer pain safety behavior.
- Added a reproducible command-line benchmark.
- Added a more complete report with data, model logic, evaluation, limitations, and next steps.
- Removed duplicate folders and Python cache files.
