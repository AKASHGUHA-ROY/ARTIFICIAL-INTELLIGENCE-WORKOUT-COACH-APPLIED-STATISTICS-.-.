# MVP Report: Workout Planner

## Executive Summary

This project is a small rule-based workout planner built as a class-project MVP. It takes a few simple user constraints such as workout focus, experience level, available time, available equipment, and basic pain information, then returns a short workout plan with a brief rationale. The current implementation uses a local JSON dataset, Python selection rules, and a simple terminal interface for custom user input. It does not use external APIs, model training, or personalized learning.

Compared with the earlier baseline demo behavior, the current MVP does a better job of prioritizing main workout movements and making short sessions feel more like real workouts instead of warmup-heavy lists.

## User & Use Case

The intended user is a beginner or casual exerciser who wants a simple workout suggestion without needing a full coaching app. A likely example is a student with limited time, limited equipment, and a need for clear, practical guidance.

The main use cases supported by the current MVP are:

- generating a focused workout for one body area
- generating a short full-body session
- filtering by available equipment
- entering custom workout preferences in the terminal
- staying more conservative when pain is reported
- giving a simple next-step response during a workout when effort or pain is reported

## System Design

The system has four main parts:

- `data/exercises.json` stores the local exercise dataset
- `src/planner.py` applies rule-based filtering, ranking, and plan construction
- `src/demo.py` runs five benchmark-style demo cases and prints the outputs
- `src/chat_demo.py` asks for user input in the terminal and prints a custom plan

## ASCII Diagram

```text
Fixed demo cases or terminal user input
  |
  v
src/demo.py or src/chat_demo.py ------+
  |                                   |
  v                                   |
src/planner.py                        |
  |                                   |
  +--> load exercises ------------> data/exercises.json
  |
  +--> filter by level, focus, equipment, pain
  |
  +--> rank exercises with simple rules
  |
  +--> build targeted or full-body plan
  |
  +--> summarize output + rationale + safety note
  |
  v
Printed workout plan
```

The fixed demo and the interactive terminal script both call the same planner function. The planner first filters exercises using the user constraints. It then ranks exercises so main workout movements are favored over warmup-like or lower-intensity options. After that, it builds either a targeted plan for one body area or a balanced full-body plan. Finally, it summarizes repeated exercise picks and returns the plan, total time, rationale, and safety note when needed.

## Data

The MVP uses one local JSON file as its exercise dataset. Each exercise entry includes fields such as:

- name
- body part
- equipment
- level
- estimated minutes
- role
- dorm-friendly flag
- pain-avoidance flags
- tags

The dataset is intentionally small and beginner-friendly. It was expanded with a small filtered subset inspired by public exercise data sources, then normalized into the existing JSON schema. This improves coverage for the benchmark cases without changing the rule-based planner design or adding external runtime dependencies.

## Models / Workflow

This project does not use a trained machine learning model. The workflow is fully rule-based.

## Workflow

- Load the exercise dataset from JSON.
- Collect fixed benchmark inputs from `src/demo.py` or custom terminal inputs from `src/chat_demo.py`.
- Filter exercises by level, focus, equipment, dorm-friendliness, and pain constraints.
- Rank exercises so stronger main movements are chosen before warmup-like moves.
- Build either a focused plan or a full-body plan.
- Summarize repeated exercise selections into a cleaner output format.
- Return the plan, total time, rationale, and safety note if needed.

This design fits the MVP because it is transparent and easy to debug. A reviewer can follow the code and understand why a given exercise was selected.

## Evaluation

The current evaluation is demo-based rather than statistical. The project still uses five benchmark-style cases in `src/demo.py`:

- beginner arm day, no equipment, 20 minutes
- intermediate back day, dumbbells only, 45 minutes
- beginner leg day with knee pain
- busy student full-body workout, 15 minutes
- user reports high effort and pain after a set

The project also includes `src/chat_demo.py`, which lets a user type their own experience level, focus, available time, equipment, busy-student preference, and optional pain area into the terminal. This is an interaction feature, not a separate evaluation method.

## Evaluation Criteria

The current MVP is judged using simple qualitative criteria:

- **Constraint matching:** Does the plan respect the requested focus, time, equipment, and pain constraints?
- **Exercise ordering:** Do main workout movements appear before warmup-like or lower-value filler movements?
- **Short-workout quality:** Does a short full-body session still feel practical and workout-like?
- **Safety behavior:** Does the planner stay conservative when pain is reported?
- **Clarity:** Is the output easy to read and supported by a short rationale?

## Current Results

The current improved outputs suggest that the planner is stronger than the earlier baseline in several visible areas:

- the no-equipment arm workout now starts with clearer main exercises and fills the 20-minute target
- the dumbbell back workout has enough relevant options to fill the 45-minute target
- the knee-pain leg workout stays conservative while still filling the 20-minute target
- the short full-body workout now fills the 15-minute target with upper-body, lower-body, and core/cardio coverage

The other demo cases also show that the planner can respect equipment limits and apply conservative pain filtering. However, this evaluation is still limited because it is based on a small set of handpicked demo cases rather than user testing or large-scale benchmarking.

## Limitations & Risks

This MVP has several important limitations:

- the exercise dataset is small, so workout variety is limited
- the planner does not generate sets, reps, or rest times
- the pain logic is broad and should not be treated as medical advice
- the rationale is short and template-like
- the system does not learn from user feedback
- the demo outputs are useful examples, but not proof of real-world effectiveness

The main risk is presenting the project as more intelligent or personalized than it really is. It is more accurate to describe it as a rule-based recommendation prototype with basic safety filters.

## Next Steps

Reasonable next steps for this MVP would be:

- continue expanding the exercise dataset carefully with more beginner-safe options
- add simple sets, reps, and rest guidance
- improve variation rules so repeated plans feel less repetitive
- make short workouts feel more like circuits instead of simple exercise lists
- add more evaluation cases, including edge and failure cases
- collect user feedback on whether the plans feel practical and understandable

These next steps would strengthen the project while keeping the current beginner-friendly, rule-based structure.
