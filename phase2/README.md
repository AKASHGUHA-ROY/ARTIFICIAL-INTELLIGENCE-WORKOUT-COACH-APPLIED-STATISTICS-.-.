# Workout Assistant Evaluation

This repository compares baseline and improved AI behavior for a workout-assistant task.

The goal is not just to generate workouts. The goal is to build an assistant that is:

- personalized
- practical
- constraint-aware
- brief when needed
- safer around pain and recovery questions
- able to replan when the original workout no longer fits

## Project Goal

This project evaluates how a raw general-purpose AI performs on realistic workout-assistant prompts before and after task-specific improvements.

The improved version focuses on four design ideas working together:

1. **Response policy** for giving the right kind of answer in the right order
2. **Substitution engine** for swapping exercises when time, space, equipment, or pain changes the plan
3. **Minimal follow-up questions** so the assistant asks only the highest-value questions
4. **Evaluation rubric** so quality can be scored consistently across test cases

## Combined Design Framework

### 1. Response Policy

The improved assistant follows a fixed response order:

1. **Immediate next action**  
   Tell the user what to do now.

2. **Safety and constraint check**  
   Screen for pain, red flags, equipment limits, time limits, or space limits.

3. **Shortest useful recommendation**  
   Give the most useful plan without over-explaining.

4. **Optional deeper layer**  
   Add more detail only when needed or when the user asks for it.

This helps prevent the baseline problem of jumping straight into long generic plans.

### 2. Substitution Engine

The improved assistant should not break when the original plan no longer fits. Instead, it should swap movements based on the user's current constraints.

Examples:

- **No equipment** -> use self-resisted, wall-based, or bodyweight alternatives
- **Knee pain** -> bias toward lower-knee-stress options and avoid deep knee-flexion by default until clarified
- **Dorm or shared space** -> remove jumping, loud foot strikes, and large-space movements
- **Short on time** -> compress the session into a fallback version instead of giving the full original plan
- **Exercise hurts** -> replace the painful movement with a nearby pattern that keeps the session productive

The goal is to make the assistant feel adaptable instead of brittle.

### 3. Minimal Follow-Up Questions

The improved assistant should ask fewer questions, but better ones.

It should ask only the highest-value questions needed to make the next response safer or more useful.

Examples:

**For pain inputs:**
- Where exactly is the pain?
- Does it feel sore, sharp, cramped, or unstable?
- Any swelling, locking, numbness, or giving way?

**For workout planning:**
- How much time do you have right now?
- What equipment do you have?
- Are you in a gym, dorm, or small shared space?

This prevents the assistant from sounding robotic or slow.

### 4. Evaluation Rubric

Each test case can be scored on a 1 to 5 scale across these categories:

| Category | What it measures | Strong output looks like |
|---|---|---|
| Personalization | Fit to user level, goal, and context | Clearly adapted to the request |
| Constraint Handling | Respect for time, equipment, pain, and setting | No hidden assumptions |
| Safety / Triage | Handling of pain or risk signals | Screens before prescribing |
| Actionability | Whether the next step is obvious | User knows what to do now |
| Brevity | Whether the response length fits the moment | Short when short is needed |
| Substitution / Replanning | Ability to adapt when the plan breaks | Good swaps and fallback plans |

A simple scoring scale:

- **1 = weak**
- **3 = acceptable**
- **5 = strong**

## Evaluation Summary

| Test Case | Baseline Quality | Improved Quality | Main Improvement | Remaining Problem |
|---|---|---|---|---|
| 1 | Weak | Strong | Better personalization and tighter fit to the 20-minute constraint | Output can still sound somewhat generic |
| 2 | Weak | Strong | Stronger handling of equipment, time, and realistic workout pacing | Replanning after missed workouts could still be clearer |
| 3 | Weak | Moderate | Safer first response and better handling of pain as a constraint | Still difficult without follow-up clarification |
| 4 | Weak | Strong | Better adaptation to short sessions, dorm life, and quiet-mode needs | Pulling options remain limited without equipment |
| 5 | Weak | Strong | More direct next-step guidance and better session-level adjustment | Pain advice still depends on limited user context |

## Outputs in This Repo

### Baseline Outputs

These are the raw answers from the original general-purpose model before any task-specific changes.

Keep these unchanged in `baseline_outputs.md` so readers can see the true baseline.

### Improved Outputs

These are rewritten answers produced after applying the improved response framework.

Keep these in a separate section or file such as `improved_outputs.md` so the repo shows a clear before-and-after comparison.

## Test Cases

### Test Case 1
**User input:** Beginner user, arm day, no equipment, 20 minutes.

**Baseline weakness:**  
The baseline response is usable, but it is too generic and not tight enough for the user's exact constraints.

### Test Case 2
**User input:** Intermediate user, back day, dumbbells only, 45 minutes.

**Baseline weakness:**  
The baseline response is reasonable, but it does not fully respect the equipment constraint and becomes too long once pacing is considered.

### Test Case 3
**User input:** Beginner user, leg day, knee pain reported.

**Baseline weakness:**  
The baseline response over-explains, mixes workout advice with rehab-style guidance, and does not prioritize the safest next action first.

### Test Case 4
**User input:** Busy student, full body workout, 15 minutes.

**Baseline weakness:**  
The baseline response gives a generic circuit, but it does not adapt well to student life, small shared spaces, or noise limits.

### Test Case 5
**User input:** User reports high effort and pain after a set and asks what to do next.

**Baseline weakness:**  
The baseline response gives caution, but it does not answer the immediate question directly enough and jumps too quickly into a bigger weekly plan.

## Repository Structure

A simple structure for this project:

- `README.md` -> project overview, design approach, and summary
- `baseline_outputs.md` -> raw baseline examples
- `improved_outputs.md` -> improved versions in a separate section or file
- `rubric.md` -> optional detailed scoring sheet
- `notes/` -> optional working notes or future ideas

## Design Principles

The improved assistant should:

- answer the immediate question first
- treat pain as a triage problem before turning it into programming advice
- ask only one or two high-value follow-ups when needed
- adapt to time, space, equipment, and user level
- offer substitutions instead of forcing the original plan
- stay concise unless the user asks for more depth

## Safety Note

This project is for fitness-assistant evaluation and planning support. It is not intended to diagnose injuries or replace medical care.

## Next Steps

Good next improvements for the project:

- add more edge-case test prompts
- score each output with the rubric instead of only using labels
- add a missed-workout replanning test case
- add a dorm-only / tiny-space-only test case
- add a one-dumbbell-only test case
- document remaining failure modes more clearly
- ## How to Run

Run the prototype demo with:

```bash
python phase2/workout_assistant_demo.py
