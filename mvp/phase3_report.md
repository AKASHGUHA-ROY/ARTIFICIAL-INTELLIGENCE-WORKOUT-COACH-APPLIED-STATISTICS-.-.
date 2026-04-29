# Phase 3 MVP Report: AI Workout Assistant

**Course:** MAE301 Applied Statistics / AI Startup Project  
**Project:** AI Workout Trainer for Personalized Exercise Guidance  
**MVP Folder:** `mvp/`  
**Team Members:** Akash Guha Roy, Jacob, Luke, Payne  
**Demo Video:** [Google Drive Demo Video](https://drive.google.com/file/d/16OGasSNzUpy7QB-oj7WTxT7jEnWmiaWw/view?usp=sharing)

---

## 1. Executive Summary

The Phase 3 MVP is an AI-style workout assistant designed for busy students, beginners, and casual exercisers who need quick, safe, and personalized workout guidance. The user enters their workout situation, including target focus, available equipment, workout duration, experience level, pain status, and current effort level. The system then generates a workout plan that attempts to fit those constraints and provides a short rationale and safety guidance.

The current MVP is implemented as a Streamlit web application with a local Python planning engine. It does not use a trained machine learning model or external API. Instead, it uses a transparent rule-based recommendation workflow built around a structured local exercise dataset. This design was chosen because the project goal for Phase 3 was to produce a working, reproducible prototype that can be inspected, run locally, and evaluated with benchmark scenarios.

The main user-facing features are:

- Personalized workout plan generation for arms, back, legs, core, or full body.
- Filtering by available equipment: no equipment, dumbbells, chair, or combinations.
- Filtering by experience level: beginner, intermediate, or advanced.
- Time-aware workout construction that keeps the plan within the user’s selected duration.
- Conservative pain-aware filtering for knee, upper-body, arm, shoulder, or back pain.
- Dorm-friendly workout mode for busy students or small spaces.
- In-the-moment coaching response when the user reports high effort or pain.
- Explanation of why the plan was selected.

The MVP was evaluated with 10 realistic benchmark scenarios. In the current evaluation run, 9 out of 10 scenarios passed all automated checks, and 45 out of 46 individual checks passed. The one failing scenario was an intentionally restrictive edge case where no safe matching plan existed. The system handled that case safely by returning no workout instead of recommending an unsafe exercise, but the benchmark still marked it as a failure because no plan was generated.

---

## 2. User & Use Case

### 2.1 Target User

The primary user is a busy student or beginner/casual exerciser who wants to work out but does not know what exercises to choose. This user may not have access to a gym, a trainer, or expensive fitness apps. They may only have a dorm room, a small apartment, dumbbells, a chair, or no equipment at all.

A secondary user is someone returning to exercise carefully after mild discomfort or soreness. The system is not designed to diagnose injuries or replace medical advice, but it can take a conservative approach when the user reports pain.

### 2.2 User Pain Point

Many fitness videos and workout apps give generic routines. They often assume the user has enough time, enough space, the right equipment, and no pain limitations. For beginners, this can create confusion because they do not know how to adjust the plan when their situation changes.

Examples of common user problems:

- “I only have 15 minutes before class.”
- “I live in a dorm and cannot jump around.”
- “I want to train legs, but my knee hurts.”
- “I only have dumbbells.”
- “The workout feels too intense and I do not know whether to keep going.”

The MVP addresses these problems by turning user constraints into a concrete workout plan and a conservative next-step recommendation.

### 2.3 Concrete Usage Narrative

A student opens the Streamlit app before class. They select:

- Focus: full body
- Equipment: no equipment
- Duration: 15 minutes
- Experience level: beginner
- Busy student / dorm-friendly: yes
- Pain: no
- Effort level: moderate

The app returns a short workout using dorm-friendly bodyweight movements, stays within the time limit, and explains that it selected exercises to cover upper body, lower body, and core/cardio as much as possible within the short session.

Another user selects:

- Focus: legs
- Equipment: no equipment
- Duration: 20 minutes
- Experience level: beginner
- Pain: knee

The planner removes knee-aggravating exercises such as bodyweight squats and chair sit-to-stands, then recommends more conservative lower-body exercises such as glute bridges, calf raises, clamshells, and side-lying leg raises.

---

## 3. MVP Scope

### 3.1 Original MVP Goal

The original project idea was an AI workout trainer that could give personalized exercise guidance and in-session next-step suggestions. The ideal long-term product could eventually include user history, live set logging, natural-language coaching, and possibly camera-based form feedback.

### 3.2 Phase 3 MVP Scope

For Phase 3, the team narrowed the scope to a text-based workout recommendation prototype. The final MVP focuses on one concrete feature:

> A user can enter their workout focus, equipment, available time, experience level, effort level, and pain status, and the system returns a safe, constraint-aware workout plan and coaching message.

This scope is realistic for the course timeline and produces a runnable prototype with measurable behavior.

### 3.3 What the MVP Does Not Yet Do

The MVP does not yet:

- Track long-term workout history.
- Learn from user feedback.
- Use a trained machine learning model.
- Use a large language model API.
- Provide camera-based form correction.
- Diagnose injuries or give medical advice.
- Provide detailed sets, reps, rest periods, or progression plans for every exercise.

These are treated as future improvements rather than Phase 3 requirements.

---

## 4. System Design

### 4.1 High-Level Architecture

```text
User
 |
 v
Streamlit Interface: mvp/app.py
 |
 | collects:
 | - target focus
 | - equipment
 | - minutes available
 | - experience level
 | - busy student / dorm-friendly flag
 | - pain status and pain area
 | - current effort level
 v
Planner Engine: mvp/src/planner.py
 |
 | loads local exercise data
 | filters exercises by constraints
 | scores and ranks candidate exercises
 | builds targeted or full-body workout
 | summarizes repeated exercises
 v
Output
 |
 | - recommended workout plan
 | - total estimated time
 | - rationale
 | - safety note
 | - in-the-moment coaching response
 v
User sees recommendation in Streamlit
```

### 4.2 Main Files

| File | Purpose |
|---|---|
| `mvp/app.py` | Streamlit user interface. Collects user inputs and displays recommendations. |
| `mvp/src/planner.py` | Main planning logic. Loads exercises, filters candidates, ranks exercises, builds plans, and returns safety guidance. |
| `mvp/src/demo.py` | Command-line demo script with representative examples. |
| `mvp/src/evaluate.py` | Automated evaluation script with 10 benchmark scenarios. |
| `mvp/data/exercises.json` | Local structured exercise dataset. |
| `mvp/artifacts/demo_outputs.md` | Saved evidence from earlier demo runs. |
| `mvp/artifacts/evaluation_results.md` | Generated evaluation results from `python src/evaluate.py`. |
| `mvp/README.md` | Setup and demo instructions. |
| `mvp/report.md` | This Phase 3 report. |

### 4.3 Input Fields

The Streamlit app collects:

- `focus`: target workout focus: arms, back, legs, core, or full body.
- `equipment`: equipment available to the user.
- `minutes_available`: requested workout duration from 5 to 60 minutes.
- `experience_level`: beginner, intermediate, or advanced.
- `busy_student`: whether the user needs dorm-friendly options.
- `pain_reported`: whether the user is feeling pain.
- `pain_area`: knee, upper body, arm, shoulder, or back if pain is reported.
- `effort_level`: current effort from 1 to 10.
- `notes`: optional user-entered notes.

### 4.4 Output Fields

The planner returns a dictionary containing:

- `plan`: a list of selected exercise rows.
- `total_minutes`: total estimated workout time.
- `rationale`: explanation of why the plan was selected.
- `safety_note`: conservative warning if pain is reported.

Each plan item includes:

- exercise name
- body part
- role
- equipment
- minutes per round
- total minutes
- number of rounds

### 4.5 Planning Workflow

The planning engine uses the following workflow:

1. **Load exercise data**  
   The planner loads `mvp/data/exercises.json`.

2. **Filter by experience level**  
   A beginner user can only receive beginner-level exercises. Intermediate and advanced users may receive easier exercises as well. This is handled using the `LEVEL_ORDER` ranking.

3. **Filter by workout focus**  
   If the user selects arms, back, legs, or core, the system only selects exercises for that body part. If the user selects full body, the planner can use the entire filtered exercise pool.

4. **Filter by equipment**  
   The system only keeps exercises where the required equipment is a subset of the user’s available equipment.

5. **Filter by dorm-friendly setting**  
   If the busy student option is enabled, the system keeps only exercises marked as `dorm_friendly`.

6. **Filter by pain constraints**  
   If the user reports knee pain, the system removes exercises marked `avoid_if_knee_pain`. If the user reports upper-body, arm, shoulder, or back pain, the system removes exercises marked `avoid_if_upper_body_pain`.

7. **Score candidate exercises**  
   Candidate exercises receive role-based and tag-based scores. Main exercises are prioritized over support and warmup exercises. Helpful tags such as strength, compound, push, pull, conditioning, and bodyweight can increase score. Warmup, mobility, or stability tags can reduce priority when building the main workout.

8. **Build workout plan**  
   - For targeted workouts, the system selects ranked exercises for the requested focus.
   - For full-body workouts, the system first attempts to cover upper body, lower body, and core/cardio buckets.

9. **Respect time limit**  
   The planner only adds an exercise if the estimated time stays within `minutes_available`.

10. **Summarize repeated exercises**  
    If an exercise is selected more than once, repeated selections are summarized as rounds instead of printing duplicate rows.

11. **Return rationale and safety note**  
    The system explains the plan and adds a conservative safety note when pain is reported.

---

## 5. Data

### 5.1 Dataset Location

The MVP uses a local exercise dataset stored at:

```text
mvp/data/exercises.json
```

No external dataset download is required to run the MVP.

### 5.2 Dataset Size

The current dataset contains **31 exercise records**.

Body-part distribution:

| Body Part | Count |
|---|---:|
| Arms | 7 |
| Back | 7 |
| Legs | 8 |
| Core | 5 |
| Full body | 4 |

Experience-level distribution:

| Level | Count |
|---|---:|
| Beginner | 24 |
| Intermediate | 7 |
| Advanced | 0 |

Exercise-role distribution:

| Role | Count |
|---|---:|
| Main | 17 |
| Support | 12 |
| Warmup | 2 |

### 5.3 Dataset Fields

Each exercise record contains:

| Field | Meaning |
|---|---|
| `name` | Exercise name shown to the user. |
| `body_part` | Primary workout focus category. |
| `equipment` | Required equipment list, such as `none`, `dumbbells`, or `chair`. |
| `level` | Minimum user experience level. |
| `estimated_minutes` | Approximate time needed for the exercise block. |
| `role` | Whether the exercise is a main exercise, support exercise, or warmup. |
| `dorm_friendly` | Whether the exercise is appropriate for a small-space student workout. |
| `avoid_if_knee_pain` | Whether the exercise should be removed if the user reports knee pain. |
| `avoid_if_upper_body_pain` | Whether the exercise should be removed if the user reports upper-body pain. |
| `tags` | Additional descriptors used for scoring and ranking. |

### 5.4 Data Cleaning and Normalization

The exercise data was normalized into consistent categories so the planner can make deterministic decisions. Examples include:

- Equipment is stored as a list instead of a single string.
- Experience levels use a fixed order: beginner, intermediate, advanced.
- Body parts use controlled labels: arms, back, legs, core, full_body.
- Pain filters are stored as boolean fields.
- Exercise roles are standardized as main, support, or warmup.

### 5.5 Data Limitations

The dataset is intentionally small and easy to inspect, but this creates limitations:

- There are no advanced-level exercises currently in the dataset.
- There are not enough chair-based exercises for every focus area.
- All current exercises are marked dorm-friendly, so the dorm-friendly filter exists in code but does not yet strongly separate noisy or non-dorm exercises from quiet exercises.
- The dataset does not include sets, reps, rest time, muscles worked, contraindications, or detailed coaching cues.
- The dataset does not include evidence-based source citations for each exercise entry.
- The system cannot cover every injury, disability, fitness goal, or equipment setup.

### 5.6 Train / Validation / Test Split

Because the Phase 3 MVP does not train a supervised model, there is no traditional train/validation/test split. Instead, the system is evaluated through benchmark scenarios that test whether the rule-based planner respects constraints such as time, equipment, focus, and pain safety.

If the project is extended with a supervised ranking model later, the exercise-selection examples should be split into training, validation, and test sets.

---

## 6. Models / AI System

### 6.1 Current Model Type

The current MVP uses a **rule-based recommendation and decision-support system**. It does not use:

- a trained neural network,
- a supervised classifier,
- a regression model,
- a generative model,
- a frontier LLM API,
- or a hosted model checkpoint.

This choice makes the prototype transparent, reliable, and easy to reproduce.

### 6.2 Why This Still Fits the AI-Enabled MVP Goal

The system behaves like a simple AI assistant because it:

1. Collects user context.
2. Interprets constraints.
3. Filters unsafe or impossible options.
4. Scores and ranks candidate actions.
5. Constructs a personalized recommendation.
6. Provides a rationale and safety-aware response.

In other words, the MVP is an agent-like workflow even though it is not a learned model. The intelligence comes from structured decision logic, not from learned parameters.

### 6.3 Scoring Logic

The planner scores exercises using role and tag information.

Role scores:

| Role | Score Contribution |
|---|---:|
| Main | +40 |
| Support | +20 |
| Warmup | +0 |

Selected tag bonuses include:

| Tag | Effect |
|---|---:|
| compound | +6 |
| conditioning | +5 |
| strength | +4 |
| bodyweight | +3 |
| push | +3 |
| pull | +3 |
| core | +2 |

Selected tag penalties include:

| Tag | Effect |
|---|---:|
| warmup | -8 |
| mobility | -3 |
| stability | -3 |
| low_impact | -2 |
| balance | -1 |

This ranking causes the planner to prefer main workout exercises before support or warmup movements.

### 6.4 Full-Body Planning Logic

For full-body workouts, the planner groups exercises into three buckets:

- upper body: arms and back
- lower body: legs
- core/cardio: core and full-body exercises

The planner tries to select at least one exercise from each bucket before filling remaining time. For very short workouts, the system may not be able to fully cover all buckets because it refuses to exceed the time limit.

### 6.5 Safety Logic

The MVP uses conservative safety behavior:

- If knee pain is reported, exercises flagged as knee-pain risks are removed.
- If upper-body, arm, shoulder, or back pain is reported, exercises flagged as upper-body-pain risks are removed.
- If pain is reported during a coaching check-in, the assistant tells the user to pause and avoid pushing through pain.
- If high effort is reported without pain, the assistant recommends longer rest and lower intensity.

This logic is intentionally cautious. The MVP is not a medical tool and should not be treated as injury diagnosis or treatment.

---

## 7. Implementation Details

### 7.1 Streamlit App

The Streamlit app is located at:

```text
mvp/app.py
```

It provides a simple user interface where the user selects workout constraints and presses **Get Recommendation**. The app then displays:

- recommended workout plan,
- total time,
- rationale,
- safety note if pain is reported,
- and in-the-moment coaching feedback.

### 7.2 Planner Module

The planner is located at:

```text
mvp/src/planner.py
```

Important functions include:

| Function | Purpose |
|---|---|
| `load_exercises()` | Loads local exercise JSON data. |
| `filter_exercises()` | Applies level, focus, equipment, dorm-friendly, and pain filters. |
| `score_exercise()` | Scores candidate exercises using role and tags. |
| `build_targeted_plan()` | Builds an arms, back, legs, or core plan. |
| `build_full_body_plan()` | Builds a full-body plan using bucket coverage. |
| `summarize_plan()` | Combines repeated exercises into clean output rows. |
| `build_workout_plan()` | Main public planner function. |
| `next_step_for_effort_and_pain()` | Gives conservative coaching advice for pain or high effort. |

### 7.3 Demo Script

The command-line demo is located at:

```text
mvp/src/demo.py
```

It runs five representative scenarios and prints the output. This is useful for quick reproduction without opening the web interface.

### 7.4 Evaluation Script

The evaluation script is located at:

```text
mvp/src/evaluate.py
```

It runs 10 benchmark scenarios and writes results to:

```text
mvp/artifacts/evaluation_results.md
```

### 7.5 Dependencies

The MVP currently requires:

```text
streamlit
```

No API key is required.

---

## 8. Demo Instructions and Reproducibility

### 8.1 Setup

From the repository root:

```bash
cd mvp
python -m venv .venv
```

Activate the virtual environment.

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 8.2 Run the Streamlit App

```bash
streamlit run app.py
```

The app should open in the browser. If it does not open automatically, Streamlit will print a local URL in the terminal.

### 8.3 Run the Command-Line Demo

```bash
python src/demo.py
```

### 8.4 Run the Evaluation

```bash
python src/evaluate.py
```

This prints evaluation results in the terminal and writes a Markdown artifact to:

```text
mvp/artifacts/evaluation_results.md
```

### 8.5 API Keys

No API keys are required for this MVP because it does not call an external model or web service.

---

## 9. Evaluation

### 9.1 Evaluation Goal

The purpose of evaluation is to test whether the MVP behaves correctly across realistic user situations. The evaluation focuses on constraint satisfaction, safety behavior, and reproducibility rather than model accuracy because the current system is rule-based.

### 9.2 Evaluation Method

The evaluation script runs 10 scenarios covering:

1. Beginner arms workout with no equipment.
2. Intermediate back workout with dumbbells.
3. Beginner legs workout with knee pain.
4. Busy student full-body workout with no equipment.
5. High effort with pain during coaching.
6. Missed workout with only 10 minutes available.
7. Shoulder or upper-body pain.
8. Dorm/quiet workout constraint.
9. Very short 5-minute workout.
10. Edge case where no safe matching exercises are available.

### 9.3 Metrics

For workout-plan scenarios, the script checks:

| Metric | Meaning |
|---|---|
| `time_ok` | Total workout time is less than or equal to the requested time. |
| `equipment_ok` | Every selected exercise only uses available equipment. |
| `pain_safe` | Exercises violating the pain constraint are removed. |
| `focus_match` | Exercises match the requested focus unless the request is full body. |
| `plan_exists` | The planner returns at least one exercise. |

For coaching scenarios, the script checks:

| Metric | Meaning |
|---|---|
| `safety_response` | If pain is reported, the message recommends stopping, pausing, reducing, resting, or using gentle movement. |

### 9.4 Quantitative Results

Current evaluation result:

| Result Type | Value |
|---|---:|
| Total scenarios | 10 |
| Scenarios passing all checks | 9 |
| Scenario pass rate | 90% |
| Individual checks passed | 45 / 46 |
| Individual check pass rate | 97.8% |

### 9.5 Scenario-Level Results

| # | Scenario | Result | Notes |
|---:|---|---|---|
| 1 | Beginner arms, no equipment, 20 minutes | PASS | Returned 18-minute arms plan using no equipment. |
| 2 | Intermediate back, dumbbells only, 45 minutes | PASS | Returned 41-minute dumbbell back plan. |
| 3 | Beginner legs with knee pain | PASS | Removed knee-pain exercises and returned conservative leg plan. |
| 4 | Busy student full-body, no equipment, 15 minutes | PASS | Returned 14-minute full-body plan with dorm-friendly exercises. |
| 5 | High effort with pain | PASS | Recommended pausing and not pushing through pain. |
| 6 | Missed workout with only 10 minutes | PASS | Returned 10-minute short workout. |
| 7 | Shoulder/upper-body pain | PASS | Avoided upper-body pain exercises and returned lower/core alternatives. |
| 8 | Dorm/quiet workout | PASS | Returned a 19-minute no-equipment plan. |
| 9 | Very short 5-minute workout | PASS | Returned one 4-minute core exercise. |
| 10 | No valid exercises available | FAIL | Safely returned no plan; failed because `plan_exists` was false. |

### 9.6 Example Evaluation Outputs

#### Example 1: Beginner arms, no equipment, 20 minutes

Input:

```json
{
  "experience_level": "beginner",
  "focus": "arms",
  "minutes_available": 20,
  "equipment": ["none"],
  "busy_student": false
}
```

Output summary:

```text
Total minutes: 18.
Exercises: Knee Push-Ups, Wall Push-Ups, Shoulder Taps.
Rationale: selected 3 exercises, kept the session to about 18 minutes,
and preferred main arms exercises before warmup-like moves.
```

Result: PASS.

#### Example 2: Beginner legs with knee pain

Input:

```json
{
  "experience_level": "beginner",
  "focus": "legs",
  "minutes_available": 20,
  "equipment": ["none"],
  "busy_student": false,
  "pain_area": "knee"
}
```

Output summary:

```text
Total minutes: 17.
Exercises: Glute Bridges, Standing Calf Raises, Clamshells, Side-Lying Leg Raises.
Rationale: removed exercises that may aggravate the reported pain.
```

Result: PASS.

#### Example 3: Edge case with no valid exercises

Input:

```json
{
  "experience_level": "beginner",
  "focus": "back",
  "minutes_available": 15,
  "equipment": ["none"],
  "busy_student": false,
  "pain_area": "shoulder"
}
```

Output summary:

```text
No plan returned.
Rationale: No safe workout was found with the current constraints.
```

Result: FAIL under the current benchmark because no plan was generated. However, this behavior is safer than recommending a back exercise that could aggravate shoulder or upper-body pain.

### 9.7 Evaluation Interpretation

The evaluation shows that the MVP performs well on common student workout scenarios. It reliably respects time limits, equipment constraints, workout focus, and pain filters in most tested cases. The system also gives conservative coaching advice when pain is reported.

The most important weakness appears in highly restrictive edge cases. When the user requests a beginner back workout with no equipment and shoulder pain, the planner cannot find a safe matching exercise. The system safely refuses to generate a plan, but from a product perspective it should do more. A better future version would explain the issue more clearly and suggest alternatives, such as a lower-body or core session that avoids the painful area.

---

## 10. Error Analysis

### 10.1 Failure Case: No Valid Exercises Available

The failed evaluation scenario requested:

- beginner level,
- back focus,
- no equipment,
- shoulder pain.

The dataset contains only one no-equipment back exercise: Reverse Snow Angels. That exercise is marked as an upper-body pain risk, so it is removed when shoulder pain is reported. As a result, there are no valid exercises remaining.

This is a good safety outcome but a weak user experience. The user receives no workout instead of a helpful replan.

Future fix:

- Add more no-equipment back exercises that are safe for some shoulder-pain cases.
- Add a fallback replan system that suggests a different focus, such as core or legs.
- Display a clearer message explaining which constraint caused the empty plan.

### 10.2 Rationale Can Overstate Full-Body Coverage

In very short full-body workouts, the planner may not have enough time to include upper body, lower body, and core/cardio. However, the rationale can still say that the plan started with full-body bucket coverage.

Future fix:

- Track which buckets were actually included.
- Only mention upper/lower/core coverage if all required buckets appear in the final selected plan.
- Otherwise say: “Because of the short time limit, this plan covers only the highest-priority available buckets.”

### 10.3 Extra Notes Are Displayed but Not Fully Used

The Streamlit app includes an “Extra notes” text area. The app displays those notes back to the user, but the current planner does not parse them into constraints.

Future fix:

- Add keyword detection for phrases such as “knee pain,” “shoulder pain,” “dorm,” “quiet,” “no jumping,” “tired,” or “no equipment.”
- Show inferred constraints transparently.
- Avoid overclaiming that the notes were deeply understood.

### 10.4 Dataset Coverage Is Limited

The small dataset makes the system easy to inspect, but it also limits workout variety. Some focus/equipment/pain combinations have very few valid options.

Future fix:

- Expand the dataset to at least 100 exercises.
- Add more beginner-safe options for each body part.
- Add more alternatives for pain-sensitive cases.
- Add sets, reps, rest time, and form cues.

### 10.5 Pain Categories Are Broad

The current system treats shoulder pain, arm pain, upper-body pain, and back pain similarly by filtering exercises marked as upper-body pain risks. This is conservative but not very precise.

Future fix:

- Add separate flags for shoulder, elbow, wrist, back, hip, ankle, and knee.
- Add pain severity and pain quality fields.
- Stop the workout entirely for sharp, worsening, unstable, or high-severity pain.

---

## 11. Limitations & Risks

### 11.1 Medical and Safety Risk

The biggest risk is that users may treat the app like a medical or professional coaching tool. It is not. The MVP does not diagnose injuries, prescribe rehabilitation, or replace a qualified trainer, doctor, or physical therapist.

The app should always communicate:

- Stop if pain is sharp, worsening, or changes normal movement.
- Do not push through pain.
- Seek professional guidance when needed.

### 11.2 Data Limitations

The exercise dataset is small, manually structured, and not comprehensive. It does not represent all users, body types, ability levels, injuries, or training goals.

### 11.3 Model Limitations

Because the MVP is rule-based, it does not learn from user behavior. It cannot automatically improve from feedback, and it may produce repetitive recommendations.

### 11.4 Personalization Limitations

The current app only considers the current session. It does not remember previous workouts, soreness history, goals, progress, or user preferences.

### 11.5 Evaluation Limitations

The evaluation uses benchmark scenarios, not a large real-user study. The test cases are useful for checking logic, but they do not prove that users will find the plans effective, enjoyable, or safe in the real world.

### 11.6 Privacy Considerations

The current MVP does not require login and does not store user data permanently. If deployed as a real product, the team would need to add clear privacy policies and protect workout history, pain reports, and personal health-related information.

### 11.7 Bias and Accessibility

The dataset mostly represents simple bodyweight and dumbbell exercises. It does not yet include enough options for users with disabilities, mobility limitations, older adults, or users with specialized training needs.

---

## 12. Next Steps

### 12.1 Highest-Priority Engineering Improvements

1. **Add detailed exercise prescriptions**  
   Add sets, reps, rest time, duration, form cues, and easier alternatives to every exercise.

2. **Improve the notes field**  
   Parse user notes into transparent constraints such as pain area, no-jumping requirement, or equipment limitations.

3. **Add better safety triage**  
   Add pain severity, pain type, and red-flag questions. Stop the workout if pain is sharp, severe, unstable, worsening, or associated with numbness or swelling.

4. **Add substitution and replanning**  
   If no safe plan exists, suggest a safer alternative workout focus instead of returning only an empty plan.

5. **Expand the exercise dataset**  
   Add more exercises across body parts, equipment types, and pain constraints.

6. **Improve full-body rationale**  
   Make the explanation match the actual buckets selected in the final plan.

7. **Add unit tests**  
   Add pytest tests for time limits, equipment filters, pain filters, and edge cases.

### 12.2 AI / ML Improvements

A future version could add a lightweight supervised ranking model. The team could create a labeled dataset of user scenarios and exercise suitability labels, then train a simple model to rerank exercises after rule-based safety filtering.

Possible features:

- focus match
- equipment match
- level match
- pain conflict
- dorm-friendly match
- role score
- estimated time

The rule-based safety filters should remain in place even if a model is added. A model should not be allowed to override safety constraints.

### 12.3 Product Improvements

Future product improvements include:

- user accounts and workout history,
- favorite exercises,
- post-workout feedback,
- adaptive progression,
- better mobile design,
- voice or chat-style interaction,
- real user interviews and usability testing.

### 12.4 Evaluation Improvements

Future evaluation should include:

- more benchmark scenarios,
- user satisfaction ratings,
- comparison against a generic workout plan baseline,
- ablation testing of scoring rules,
- tests for edge cases and unsafe inputs,
- and real student feedback from usability sessions.

---

## 13. Phase 3 Rubric Alignment

| Rubric Area | Evidence in MVP |
|---|---|
| Problem-Solution Fit | Focuses on busy students and beginners who need fast, constraint-aware workout guidance. |
| Usefulness / Impact | Produces immediate workout plans for realistic time, equipment, and pain constraints. |
| Technical Depth & Use of AI | Implements context collection, filtering, scoring, ranking, full-body planning, safety logic, and coaching responses. |
| Quality of Evaluation & Reflection | Includes 10 scenario benchmark, pass/fail metrics, result artifact, and error analysis. |
| Demo Quality & Reproducibility | Streamlit app, command-line demo, evaluation script, local data, no API key required. |

---

## 14. Conclusion

The Phase 3 MVP successfully demonstrates a working AI-style workout assistant. It collects user constraints, filters and ranks exercises, builds a personalized workout plan, and gives conservative coaching guidance when pain or high effort is reported.

The project’s strongest areas are reproducibility, transparent planning logic, and constraint-aware recommendations. The evaluation shows that the system passes most realistic benchmark scenarios and safely avoids recommending exercises when constraints make a plan unsafe.

The biggest limitations are the small exercise dataset, the lack of a trained model, limited pain triage, no detailed sets/reps/rest guidance, and weak fallback behavior when no valid exercise exists. These are realistic next steps for turning the MVP into a stronger product.

Overall, this MVP meets the Phase 3 goal of building a runnable AI-enabled product prototype with documented design, data, evaluation, limitations, and future improvements.
