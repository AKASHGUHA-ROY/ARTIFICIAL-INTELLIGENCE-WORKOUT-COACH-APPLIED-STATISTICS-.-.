# AI Workout Assistant MVP

## Overview

This MVP is a simple AI-style workout assistant for busy students and beginner/casual exercisers. The user enters their workout situation, including target focus, available equipment, workout time, experience level, pain status, and effort level. The app then returns a safe workout recommendation.

The MVP uses a rule-based workout planner instead of a trained machine learning model. The planner uses a local exercise dataset and simple Python logic to filter, rank, and select exercises based on user constraints.

## What the MVP does

The assistant can:

- generate a workout for arms, back, legs, core, or full body
- adjust for available equipment
- keep workouts within the user's available time
- use dorm-friendly options for busy students
- stay conservative when pain is reported
- give an in-the-moment safety response for high effort or pain
- explain why the plan was selected

## Project structure

```text
mvp/
├── README.md
├── report.md
├── requirements.txt
├── app.py
├── data/
│   └── exercises.json
├── src/
│   ├── planner.py
│   └── demo.py
└── artifacts/
    └── demo_outputs.md
