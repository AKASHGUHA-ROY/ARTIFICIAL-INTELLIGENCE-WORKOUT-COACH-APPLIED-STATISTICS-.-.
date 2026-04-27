# MVP Report: AI Workout Assistant

## 1. Executive Summary

This project builds an AI-style workout assistant MVP for busy students and beginner/casual exercisers. The MVP helps a user quickly generate a safe workout plan based on their available time, target workout focus, available equipment, experience level, effort level, and pain status.

The final MVP includes a Streamlit web app and a rule-based workout planner. The user enters their workout situation into the app, and the system returns a recommended workout plan, total time, rationale, safety note, and in-the-moment coaching response.

The current version does not use a trained machine learning model. Instead, it uses a transparent rule-based recommendation system with a local exercise dataset. This makes the MVP easy to run, debug, and explain for a class project.

## 2. User & Use Case

The intended user is a busy student or beginner/casual exerciser who wants quick workout guidance without needing a full coaching app or gym trainer.

A typical user may have:

- limited time
- limited equipment
- a small dorm or apartment space
- beginner-level experience
- uncertainty about what exercise to do next
- mild pain or discomfort that requires conservative guidance

Example use case:

A busy student has only 15 to 20 minutes before class and wants a simple full-body or targeted workout. They enter their available equipment, experience level, workout focus, and pain status. The app returns a short workout plan that fits their constraints and explains why the plan was selected.

## 3. System Design

The system has four main parts:

- `app.py`: Streamlit user interface
- `src/planner.py`: rule-based workout planner
- `data/exercises.json`: local exercise dataset
- `src/demo.py`: benchmark-style command-line demo cases

## ASCII Architecture Diagram

~~~text
User input from Streamlit app
  |
  v
mvp/app.py
  |
  v
src/planner.py
  |
  +--> load exercises from data/exercises.json
  |
  +--> filter by:
  |       - experience level
  |       - workout focus
  |       - available equipment
  |       - dorm-friendly need
  |       - pain constraints
  |
  +--> rank exercises using simple scoring rules
  |
  +--> build targeted or full-body plan
  |
  +--> summarize repeated exercises
  |
  v
Workout recommendation displayed in Streamlit
~~~

The planner first loads exercises from a local JSON file. It then removes exercises that do not match the user's constraints. After filtering, it ranks exercises so main workout movements are preferred over warmup-like or lower-value filler movements. For full-body workouts, it tries to include upper-body, lower-body, and core/cardio coverage. Finally, it returns a readable plan with total time, rationale, and safety notes.

## 4. Data

The MVP uses a local exercise dataset stored in:

~~~text
mvp/data/exercises.json
~~~

Each exercise entry includes fields such as:

- exercise name
- body part
- required equipment
- experience level
- estimated minutes
- exercise role
- dorm-friendly flag
- knee pain avoidance flag
- upper-body pain avoidance flag
- tags

The dataset is intentionally small and beginner-friendly. This makes the project easier to understand and edit, but it also limits workout variety and real-world coverage.

## 5. Models / AI System

This MVP does not use a trained machine learning model or external API. It uses a rule-based planning workflow.

The workflow includes:

1. Loading a structured exercise dataset.
2. Filtering exercises by user constraints.
3. Ranking exercises using simple scoring rules.
4. Building either a targeted workout or full-body workout.
5. Returning a readable recommendation with rationale and safety guidance.

Even though this is not a trained model, it still represents an AI-style assistant workflow because it takes user context, applies decision logic, and produces a personalized recommendation.

The main advantage of this approach is transparency. A reviewer can inspect the code and understand exactly why a plan was selected.

## 6. Evaluation

The MVP was evaluated using both a live Streamlit demo and benchmark-style test cases.

The command-line demo in `src/demo.py` includes five sample scenarios:

1. Beginner arm day, no equipment, 20 minutes.
2. Intermediate back day, dumbbells only, 45 minutes.
3. Beginner leg day with knee pain.
4. Busy student full-body workout, no equipment, 15 minutes.
5. User reports high effort and pain after a set.

## Evaluation Criteria

The current MVP was judged using qualitative criteria:

- **Constraint matching:** Does the plan respect the user's focus, time, equipment, and pain constraints?
- **Exercise ordering:** Are main workout movements prioritized before warmup-like movements?
- **Short-workout quality:** Does a short workout still feel practical and useful?
- **Safety behavior:** Does the assistant stay conservative when pain is reported?
- **Clarity:** Is the output easy to read and supported by a clear rationale?
- **Reproducibility:** Can the demo be run from the repository instructions?

## Current Results

The MVP successfully generates workout plans for different user situations.

For a beginner arm day with no equipment, the planner selects exercises like knee push-ups, wall push-ups, and shoulder taps. This gives the user a practical upper-body workout without requiring gym equipment.

For an intermediate back day with dumbbells, the planner prioritizes rowing movements and other main back exercises before support work.

For a beginner leg day with knee pain, the planner removes knee-aggravating exercises and returns a conservative plan with exercises such as glute bridges, calf raises, clamshells, and side-lying leg raises.

For a busy student full-body workout, the planner selects a short workout that includes upper-body, lower-body, and conditioning coverage.

For pain after a set, the assistant recommends pausing the workout and not pushing through pain.

Saved output evidence is included in:

~~~text
mvp/artifacts/demo_outputs.md
~~~

## 7. Limitations & Risks

The MVP has several limitations:

- The exercise dataset is small.
- The planner does not yet provide detailed sets, reps, or rest periods.
- Pain logic is broad and cannot diagnose injuries.
- The system does not learn from user feedback.
- The recommendation rationale is still template-like.
- The system is rule-based and does not use a trained AI model.
- The evaluation is based on sample demo cases, not real user testing.

The main risk is presenting the system as more medically or personally intelligent than it actually is. The MVP should be described as a rule-based workout recommendation prototype, not a professional coach or medical tool.

## 8. Next Steps

With 2 to 3 more months, the next improvements would be:

- Expand the exercise dataset with more beginner-safe options.
- Add sets, reps, rest times, and intensity guidance.
- Improve short workouts so they feel more like circuits.
- Add better exercise substitution logic.
- Add more pain and safety categories.
- Collect user feedback from students.
- Add memory so the app can remember previous workouts.
- Add more benchmark and edge cases.
- Improve the Streamlit interface visually.
- Explore using an LLM to explain recommendations in more natural language while keeping safety rules.
