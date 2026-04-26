# MVP Report: Workout Planner

## Executive Summary

This project is a small rule-based workout planner built as a class-project MVP. It takes a few simple user constraints such as workout focus, experience level, available time, available equipment, and basic pain information, then returns a short workout plan with a brief rationale. The current implementation uses a local JSON dataset and Python selection rules only. It does not use external APIs, model training, or personalized learning.

Compared with the earlier baseline demo behavior, the current MVP does a better job of prioritizing main workout movements and making short sessions feel more like real workouts instead of warmup-heavy lists.

## User & Use Case

The intended user is a beginner or casual exerciser who wants a simple workout suggestion without needing a full coaching app. A likely example is a student with limited time, limited equipment, and a need for clear, practical guidance.

The main use cases supported by the current MVP are:

- generating a focused workout for one body area
- generating a short full-body session
- filtering by available equipment
- staying more conservative when pain is reported
- giving a simple next-step response during a workout when effort or pain is reported

## System Design

The system has three main parts:

- `data/exercises.json` stores the local exercise dataset
- `src/planner.py` applies rule-based filtering, ranking, and plan construction
- `src/demo.py` runs five benchmark-style demo cases and prints the outputs

## ASCII Diagram

```text
User constraints
  |
  v
src/demo.py ----------------------+
  |                               |
  v                               |
src/planner.py                    |
  |                               |
  +--> load exercises --------> data/exercises.json
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
Printed demo results
```

The planner first filters exercises using the user constraints. It then ranks exercises so main workout movements are favored over warmup-like or lower-intensity options. After that, it builds either a targeted plan for one body area or a balanced full-body plan. Finally, it summarizes repeated exercise picks and returns the plan, total time, rationale, and safety note when needed.

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

The dataset is intentionally small and beginner-friendly. That keeps the project easy to understand and edit, but it also limits workout variety and real-world coverage.

## Models / Workflow

This project does not use a trained machine learning model. The workflow is fully rule-based.

## Workflow

- Load the exercise dataset from JSON.
- Filter exercises by level, focus, equipment, dorm-friendliness, and pain constraints.
- Rank exercises so stronger main movements are chosen before warmup-like moves.
- Build either a focused plan or a full-body plan.
- Summarize repeated exercise selections into a cleaner output format.
- Return the plan, total time, rationale, and safety note if needed.

This design fits the MVP because it is transparent and easy to debug. A reviewer can follow the code and understand why a given exercise was selected.

## Evaluation

The current evaluation is demo-based rather than statistical. The project uses five benchmark-style cases in `src/demo.py`:

- beginner arm day, no equipment, 20 minutes
- intermediate back day, dumbbells only, 45 minutes
- beginner leg day with knee pain
- busy student full-body workout, 15 minutes
- user reports high effort and pain after a set

## Evaluation Criteria

The current MVP is judged using simple qualitative criteria:

- **Constraint matching:** Does the plan respect the requested focus, time, equipment, and pain constraints?
- **Exercise ordering:** Do main workout movements appear before warmup-like or lower-value filler movements?
- **Short-workout quality:** Does a short full-body session still feel practical and workout-like?
- **Safety behavior:** Does the planner stay conservative when pain is reported?
- **Clarity:** Is the output easy to read and supported by a short rationale?

## Current Results

The current improved outputs suggest that the planner is stronger than the earlier baseline in two visible areas:

- the no-equipment arm workout now starts with a clearer main exercise instead of opening with warmup-like movements
- the short full-body workout now feels more like a real quick session by using stronger workout-style moves

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

- expand the exercise dataset with more beginner-safe options
- add simple sets, reps, and rest guidance
- improve variation rules so repeated plans feel less repetitive
- make short workouts feel more like circuits instead of simple exercise lists
- add more evaluation cases, including edge and failure cases
- collect user feedback on whether the plans feel practical and understandable

These next steps would strengthen the project while keeping the current beginner-friendly, rule-based structure.
