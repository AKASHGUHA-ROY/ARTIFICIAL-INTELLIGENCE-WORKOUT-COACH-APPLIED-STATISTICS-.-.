# Phase 2 Report

## Objective and Current MVP Definition

The goal of Phase 2 is to improve a general-purpose AI into a more useful workout assistant for realistic user requests. The baseline system can produce plausible workouts, but it often responds with answers that are too generic, too long, weak at handling constraints, and not careful enough when pain or recovery concerns appear.

The current MVP is not a full production app. It is a design-and-evaluation prototype with three main parts:

1. A fixed set of realistic test cases that represent common workout-assistant requests.
2. A baseline-vs-improved comparison built from stored outputs.
3. A small Python demo script that reads the Markdown artifacts and prints a comparison report.

For this phase, success means the improved system is visibly better than the baseline on the core dimensions that matter for this task:

- personalization
- constraint handling
- actionability
- brevity
- safer pain handling
- substitution or fallback behavior when the original plan no longer fits

In other words, the MVP should show that the assistant is becoming more coach-like and less generic, even before a full live model integration is built.

## What Has Been Built So Far

The repo currently contains the main pieces needed to demonstrate the Phase 2 concept.

### 1. Evaluation README
`phase2/README.md` explains the project goal, the design framework, the evaluation rubric, and the test-case summary. It defines the improved system around four connected ideas:

- response policy
- substitution engine
- minimal follow-up questions
- evaluation rubric

### 2. Test Cases
`phase2/artifacts/test_cases.md` includes five realistic prompts:

1. Beginner user, arm day, no equipment, 20 minutes.
2. Intermediate user, back day, dumbbells only, 45 minutes.
3. Beginner user, leg day, knee pain reported.
4. Busy student, full body workout, 15 minutes.
5. User reports high effort and pain after a set and asks what to do next.

These cases were chosen because they stress different failure modes instead of testing only easy workout generation.

### 3. Baseline Outputs
`phase2/artifacts/baseline_outputs.md` stores raw outputs from the original general-purpose system. These baseline answers are useful because they show the exact kinds of problems the improved assistant needs to solve:

- hidden equipment assumptions
- overly long explanations
- weak personalization
- poor adaptation to student schedules or small spaces
- unclear immediate guidance when pain is reported

### 4. Improved Outputs
`phase2/artifacts/improved_outputs.md` contains revised responses for the same five cases. These improved outputs are intentionally shorter, more constraint-aware, and more direct.

### 5. Supporting Evaluation Artifacts
The repo also includes:

- `phase2/artifacts/comparison_table.md`
- `phase2/artifacts/failure_analysis.md`

These files are useful for analysis, although they are not fully complete yet.

### 6. Demo Script
`phase2/workout_assistant_demo.py` is a simple Python script that reads the Markdown files, extracts the five test cases, and prints a comparison report with heuristic scoring.

This script is valuable because it turns the project from a purely written comparison into a lightweight runnable demo.

## Technical Approach

The Phase 2 system improvement is based on changing the response policy rather than just rewriting wording.

### 1. Response Policy
The improved assistant is designed to answer in a fixed order:

1. immediate next action
2. safety and constraint check
3. shortest useful recommendation
4. optional deeper layer only if needed

This structure is especially important for pain-related prompts. Instead of dumping a long weekly plan, the assistant should first tell the user what to do now.

### 2. Substitution Engine
The assistant should not fail when the original plan no longer fits. It should substitute movements or reduce session complexity based on the user’s situation.

Examples used in this phase include:

- using bodyweight or self-resisted options for no-equipment requests
- removing bench assumptions from dumbbell-only requests
- simplifying routines for busy students
- using lighter, lower-risk alternatives when pain is reported

### 3. Minimal Follow-Up Questions
The design avoids asking too many questions. Instead, it aims to ask only the highest-value follow-up questions needed for a safer or more useful answer.

This prevents the assistant from sounding slow or overly robotic.

### 4. Evaluation Rubric
The project uses a structured rubric to judge quality. The key categories are:

- personalization
- constraint handling
- safety / triage
- actionability
- brevity
- substitution / replanning

This makes the evaluation more systematic than simply saying that one answer “sounds better.”

### 5. Artifact-Driven MVP
A notable feature of this phase is that the system is still artifact-driven rather than fully model-driven. The repository stores the baseline and improved outputs directly in Markdown, then uses the demo script to compare them.

That means this phase is focused on response design and evaluation logic, not yet on production deployment.

## Evidence of Progress

The strongest evidence of progress is that the improved outputs consistently move in the intended direction across all five cases.

### Qualitative Improvements by Case

**Test Case 1: Beginner, arm day, no equipment, 20 minutes**  
The improved response is shorter and better aligned to the beginner and time constraints. It still needs a stricter interpretation of “no equipment,” but it is clearly tighter than the baseline.

**Test Case 2: Intermediate, back day, dumbbells only, 45 minutes**  
The improved version removes the bench assumption, simplifies pacing, and makes the session more realistic for a busy student.

**Test Case 3: Beginner, leg day, knee pain reported**  
The improved version shows one of the clearest gains. Instead of a long rehab-style answer, it starts with the safest immediate next step and avoids risky knee-loading suggestions.

**Test Case 4: Busy student, full body, 15 minutes**  
The improved version is more realistic for a shared dorm or small space and avoids the baseline’s tendency to over-explain.

**Test Case 5: Pain after a set, what next**  
The improved response finally answers the user’s actual question first. It distinguishes likely fatigue from more concerning pain signals without turning into a long weekly program.

### Simple Quantitative Signals

Using the current artifact files, the average output length dropped from about **489 words** in the baseline set to about **158 words** in the improved set. That is a reduction of roughly **67.7%**.

This matters because one of the major baseline problems was verbosity. The improved outputs are much more likely to fit the moment when a user wants a quick answer.

A lightweight heuristic scoring pass using the categories embedded in the demo script also showed an average increase from **3.76** to **4.16** across the five cases. This heuristic is not a final metric, but it still supports the qualitative judgment that the improved outputs are more usable overall.

### Case-by-Case Snapshot

| Test Case | Baseline Words | Improved Words | Main Direction of Improvement |
|---|---:|---:|---|
| 1 | 186 | 151 | Shorter, more constraint-aware beginner arm plan |
| 2 | 491 | 191 | Removes extra-equipment assumptions and tightens pacing |
| 3 | 778 | 132 | Safer and much more direct pain handling |
| 4 | 350 | 169 | Better fit for dorm life and limited time |
| 5 | 641 | 146 | Answers the immediate next-step question first |

Overall, the evidence suggests the current design framework is moving the assistant in the right direction.

## Current Limitations and Open Risks

The project has clear progress, but it is not complete.

### 1. No Live Model Integration Yet
The current repo compares stored baseline and improved outputs. It does not yet call a live model and apply the response policy dynamically at runtime.

### 2. Small Test Set
There are only five test cases. They cover useful scenarios, but they are not enough to claim broad robustness.

Important missing cases include:

- missed-workout replanning
- one-dumbbell-only setup
- quiet-mode only in a shared dorm
- shoulder pain or low-back pain variants
- very short fallback sessions such as 5 to 10 minutes

### 3. Pain Handling Is Better, But Still Limited
The improved system handles pain more cautiously than the baseline, but it still does not use true symptom-based follow-up logic. In a stronger version, the assistant would distinguish more clearly between soreness, sharp pain, instability, swelling, and other red flags.

### 4. Hidden Assumptions Still Exist
Some improved responses still rely on environment assumptions such as access to a chair or desk. That is better than the baseline, but not perfect constraint handling.

### 5. Evaluation Artifacts Are Incomplete
The repo still contains partially finished evaluation files. For example, `comparison_table.md` and `failure_analysis.md` are not fully completed for all five cases.

### 6. Demo Script Needs a Small Repo-Layout Fix
The current Python script expects `baseline_outputs.md` and `improved_outputs.md` to be in the same folder as the script, but in the current repo they live under `phase2/artifacts/`. That means the script needs a path update before it cleanly runs against the actual artifact files.

### 7. Heuristic Scoring Is Still Shallow
The current scoring logic is useful as a rough prototype, but it mostly rewards keyword presence and short answers. It is not a substitute for human evaluation.

## Plan for Phase 3

Phase 3 should focus on turning this from a strong evaluation prototype into a more complete and reliable assistant system.

### 1. Finish the Evaluation Package
Complete the supporting files so the repo tells one consistent story:

- finish `comparison_table.md`
- finish `failure_analysis.md`
- add a root-level README or clearer entry point
- make sure all artifact files agree with each other

### 2. Fix the Demo Script
Update `workout_assistant_demo.py` so it reads from `phase2/artifacts/` by default and handles missing files more gracefully.

### 3. Expand the Test Suite
Add more edge cases that stress substitution and replanning, especially:

- missed workout, only 10 minutes available
- no floor space
- one dumbbell only
- quiet dorm routine
- mild soreness vs. red-flag pain

### 4. Improve the Scoring Method
Use the rubric more explicitly and consider adding human ratings for each case. A stronger Phase 3 evaluation would include side-by-side scoring with written justification.

### 5. Add Runtime Behavior
Move beyond stored artifacts and build a small interactive demo that can take a user prompt and generate a response using the project’s rules.

### 6. Improve Pain-Aware Substitutions Carefully
If the project expands pain handling, the goal should be a safer decision layer rather than medical diagnosis. A good direction would be to build a small library of symptom-aware substitutions and red-flag checks, potentially informed by reputable physical-therapy-style guidance without presenting the system as a clinician.

## Conclusion

Phase 2 successfully establishes the core direction of the project: a workout assistant should not just generate workouts, it should adapt to real-world constraints and respond safely when conditions change.

The baseline system shows common failure modes such as verbosity, weak constraint handling, and poor immediate guidance. The improved system is not complete, but it already demonstrates meaningful gains in brevity, actionability, and safety-aware behavior.

The project is now in a good position for Phase 3, where the main challenge is to turn the current design-and-evaluation framework into a more automated and more rigorous assistant system.
