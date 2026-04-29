# MVP Report: AI Workout Assistant

## 1. Executive Summary

This project is an AI-style workout assistant MVP for busy students and beginner lifters. The problem is that many people want to exercise, but they do not always know what to do when they have limited time, limited equipment, a small space, or some pain that makes them unsure about what is safe.

The MVP includes a Streamlit web app, a local exercise dataset, and a rule-based workout planner. The user enters their workout focus, available equipment, time, experience level, dorm-friendly needs, pain status, and effort level. The system returns a workout plan, estimated time, sets and reps style guidance, rest suggestions, form cues, rationale, and safety notes.

This version does not use a trained machine learning model. It uses a transparent rule-based recommendation system. This makes the MVP easier to run, debug, and explain for a class project.

## 2. User and Use Case

The intended user is a busy student, beginner lifter, or casual exerciser who wants quick workout guidance without paying for a coach or using a complicated fitness app.

A typical user may have these constraints:

- Only 10 to 30 minutes available
- Little or no equipment
- A dorm room or apartment space
- Beginner-level exercise knowledge
- Uncertainty about what exercise to choose
- Pain or discomfort that requires conservative guidance

Example use case:

A student has 15 minutes before class and wants a quick full-body workout in a small room. They select no equipment, beginner experience, full-body focus, and dorm-friendly mode. The assistant returns a short plan with upper-body, lower-body, and core or conditioning work.

## 3. System Design

The system has four main parts:

- `app.py`: Streamlit user interface
- `src/planner.py`: rule-based workout planning logic
- `data/exercises.json`: local exercise dataset
- `src/demo.py`: reproducible benchmark demo

```text
User input
  |
  v
Streamlit app
  |
  v
Planner logic
  |
  +--> Load local exercise dataset
  |
  +--> Filter by level, focus, equipment, dorm need, and pain flags
  |
  +--> Score and rank exercises
  |
  +--> Build a targeted or full-body plan
  |
  +--> Add prescription, rest time, form cue, rationale, and safety note
  |
  v
Workout plan shown to user
```

The system does not need an internet connection or API key. The planner uses the same logic in both the Streamlit app and the command-line demo.

## 4. Data

The MVP uses a local JSON dataset stored in:

```text
data/exercises.json
```

The dataset has 31 exercise entries. Each entry includes:

- Exercise name
- Body part
- Required equipment
- Experience level
- Estimated minutes
- Exercise role
- Dorm-friendly flag
- Knee pain avoidance flag
- Upper-body pain avoidance flag
- Tags

The dataset was manually structured for the MVP. It was cleaned into a consistent format so every exercise uses the same field names. The dataset is small on purpose because the goal is to demonstrate the product workflow clearly.

There is no train, validation, or test split because this MVP is not a trained supervised model. Instead, the dataset acts like a small knowledge base used for filtering and ranking.

## 5. Models and AI System

This MVP uses a rule-based recommendation workflow. The workflow is:

1. Load exercises from the JSON dataset.
2. Filter exercises based on user constraints.
3. Remove exercises that may be unsafe when pain is reported.
4. Score remaining exercises using simple priority rules.
5. Build either a targeted plan or a balanced full-body plan.
6. Add readable workout details and safety notes.

This still functions like an AI-style assistant because it uses user context to produce a personalized answer. The main difference is that it is not trained from data. It is explainable and predictable.

The system gives priority to useful main exercises over warmups or filler movements. For full-body plans, it tries to include upper-body, lower-body, and core or conditioning coverage.

## 6. Evaluation

The MVP was evaluated using five benchmark workout scenarios and one safety check-in scenario. These cases are stored in:

```text
artifacts/demo_outputs.md
```

They can be regenerated with:

```bash
python src/demo.py
```

| Case | Main Constraint Tested | Passed? |
|---:|---|---:|
| 1 | Focus, equipment, and time | Yes |
| 2 | Experience level, equipment, and main back movements | Yes |
| 3 | Pain filter, time, and useful safe alternatives | Yes |
| 4 | Short session, dorm-friendly options, and balance | Yes |
| 5 | Conservative pain behavior and fallback handling | Yes |
| 6 | Safety response for high effort and pain | Yes |

The main evaluation criteria were:

- Does the plan match the requested focus?
- Does the plan respect available equipment?
- Does the plan stay within the user time limit?
- Does the app use conservative logic when pain is reported?
- Is the output easy to understand?
- Can the demo be reproduced from the repository?

The MVP passed all six planned checks. The strongest result is that the system gives a usable plan while also explaining why it chose that plan.

## 7. Limitations and Risks

The MVP has several limitations:

- The dataset is small.
- The app does not learn from user feedback yet.
- The planner does not know the user's training history.
- Pain handling is broad and cannot diagnose injuries.
- The output is still simple compared to a real coaching app.
- The evaluation uses sample cases instead of real user testing.
- The rule-based system is less flexible than a trained model or LLM-powered assistant.

The biggest risk is making the system sound more medically advanced than it is. The app should be described as a workout planning prototype, not a medical tool or professional coaching replacement.

## 8. Next Steps

With 2 to 3 more months, the best improvements would be:

- Expand the exercise dataset.
- Add more equipment options.
- Add user goals like strength, fat loss, muscle gain, or conditioning.
- Add better sets, reps, and progression logic.
- Add exercise substitutions when the plan has limited matches.
- Add user feedback so the app can improve future workouts.
- Test the app with real students.
- Add charts for weekly consistency or workout history.
- Use an LLM only for explanation while keeping the safety rules controlled.
