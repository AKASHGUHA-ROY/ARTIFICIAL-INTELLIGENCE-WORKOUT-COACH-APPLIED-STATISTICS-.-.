
# Workout Assistant Evaluation

This repository evaluates how a raw general-purpose AI performs on a workout-assistant task before and after task-specific improvements.

## Project Goal

The goal of this project is to compare:

- **Baseline behavior** from a general-purpose AI
- **Improved behavior** after adding better personalization, constraint handling, safety behavior, and replanning

We use a small set of test cases to see where the baseline system fails and where the improved system performs better.

## What We Are Testing

The assistant is expected to do more than generate generic workouts. It should respond well to real user constraints such as:

- available time
- equipment limitations
- user experience level
- pain or safety concerns
- student schedules
- need for quick replanning

## Evaluation Summary

| Test Case | Baseline Quality | Improved Quality | Main Improvement | Remaining Problem |
|---|---|---|---|---|
| 1 | Weak | Strong | Better personalization and tighter fit to the 20-minute constraint | Output can still sound somewhat generic |
| 2 | Weak | Strong | Stronger handling of equipment, time, and busy-student constraints | Replanning after missed workouts could be clearer |
| 3 | Weak | Moderate | Safer first response and better handling of pain as a constraint | Still difficult without follow-up clarification |
| 4 | Weak | Strong | Better adaptation to short sessions and busy-student needs | Shared-space and noise constraints could be handled better |
| 5 | Weak | Strong | More direct next-step guidance and better session-level adjustment | Pain advice still depends on limited user context |

## Test Cases

### Test Case 1
**User input:** Beginner user, arm day, no equipment, 20 minutes.

**Baseline assessment:**  
The baseline response gives a usable workout, but it is not very personalized and feels too time-heavy for the request.

**Main issues:**
- not personalized enough
- too time-consuming
- still somewhat generic

---

### Test Case 2
**User input:** Intermediate user, back day, dumbbells only, 45 minutes.

**Baseline assessment:**  
The baseline response gives a reasonable workout, but it does not fully respect the user's constraints and relies on only surface-level personalization.

**Main issues:**
- too generic
- weak personalization
- not fully consistent with “dumbbells only”
- likely too long once rest and transitions are included
- not designed for a busy student schedule
- no missed-workout replanning

---

### Test Case 3
**User input:** Beginner user, leg day, knee pain reported.

**Baseline assessment:**  
The baseline response becomes too long, mixes fitness advice with rehab-style guidance, and does not clearly prioritize the safest next step.

**Main issues:**
- too detailed for the input
- not actually very personalized
- includes potentially risky exercise suggestions
- blends workout advice with medical-style guidance
- does not clarify the safest action first
- weak constraint handling

---

### Test Case 4
**User input:** Busy student, full body workout, 15 minutes.

**Baseline assessment:**  
The baseline response gives a standard short workout, but it does not really adapt to the user's real context.

**Main issues:**
- very generic
- weak connection to the student-specific problem
- assumes all exercises are appropriate
- no dynamic replanning
- may be too difficult for some users
- not clearly realistic for dorms or small shared spaces
- no quiet-mode adaptation

---

### Test Case 5
**User input:** User reports high effort and pain after a set and asks what to do next.

**Baseline assessment:**  
The baseline response contains useful caution, but it does not answer the immediate question directly enough and jumps too quickly into a weekly plan.

**Main issues:**
- does not answer the immediate question directly enough
- not personalized to the actual pain event
- jumps too quickly to a full weekly plan
- does not separate normal fatigue from urgent red flags early enough
- no session-level adjustment
- no context-aware replanning

## Key Takeaways

Across the test cases, the baseline system tends to:

- give generic answers
- over-explain when the user needs a fast response
- handle constraints inconsistently
- miss student-specific needs
- give weak session-level replanning
- respond awkwardly to pain and safety situations

The improved system performs better by:

- personalizing to the user's constraints
- giving more realistic short-session plans
- handling safety concerns more carefully
- adapting better to busy schedules
- providing more useful next-step guidance
