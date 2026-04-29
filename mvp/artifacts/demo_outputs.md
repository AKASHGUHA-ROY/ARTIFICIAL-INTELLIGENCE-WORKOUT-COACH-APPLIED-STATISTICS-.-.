# MVP Demo Outputs

This file records benchmark-style outputs from the finalized Phase 3 MVP workout planner. These examples match the current behavior of `mvp/src/demo.py` and the Streamlit app in `mvp/app.py`.

## Test Case 1: Beginner arm day, no equipment, 20 minutes

**User input:**

- Target workout focus: arms
- Available equipment: no equipment
- Workout duration: 20 minutes
- Experience level: beginner
- Busy student / dorm-friendly: optional
- Pain status: no
- Current effort level: 6

**Output:**

1. **Knee Push-Ups** | 10 min total | 2 round(s) | equipment: none
2. **Wall Push-Ups** | 4 min total | 1 round | equipment: none
3. **Shoulder Taps** | 4 min total | 1 round | equipment: none

**Total time:** 18 min

**Why this plan:** selected 3 exercise(s). kept the session to about 18 minute(s). preferred main arms exercises before warmup-like moves.

**Notes:** This output is useful because the plan begins with main upper-body movements instead of only warmup-style movements. A remaining weakness is that the no-equipment arm exercise pool is still small.

## Test Case 2: Intermediate back day, dumbbells only, 45 minutes

**User input:**

- Target workout focus: back
- Available equipment: dumbbells only
- Workout duration: 45 minutes
- Experience level: intermediate
- Busy student / dorm-friendly: optional
- Pain status: no
- Current effort level: 6

**Output:**

1. **Chest-Supported Dumbbell Rows** | 8 min total | 1 round | equipment: dumbbells
2. **Bent-Over Dumbbell Rows** | 7 min total | 1 round | equipment: dumbbells
3. **Single-Arm Dumbbell Rows** | 7 min total | 1 round | equipment: dumbbells
4. **Dumbbell Pullovers** | 7 min total | 1 round | equipment: dumbbells
5. **Rear Delt Raises** | 6 min total | 1 round | equipment: dumbbells
6. **Dumbbell Reverse Fly** | 6 min total | 1 round | equipment: dumbbells

**Total time:** 41 min

**Why this plan:** selected 6 exercise(s). kept the session to about 41 minute(s). preferred main back exercises before warmup-like moves.

**Notes:** This output is useful because larger rowing movements are prioritized before support exercises. A remaining weakness is that the planner does not yet assign detailed sets, reps, or rest periods.

## Test Case 3: Beginner leg day with knee pain

**User input:**

- Target workout focus: legs
- Available equipment: no equipment
- Workout duration: 20 minutes
- Experience level: beginner
- Busy student / dorm-friendly: optional
- Pain status: yes
- Pain area: knee
- Current effort level: 6

**Output:**

1. **Glute Bridges** | 5 min total | 1 round | equipment: none
2. **Standing Calf Raises** | 4 min total | 1 round | equipment: none
3. **Clamshells** | 4 min total | 1 round | equipment: none
4. **Side-Lying Leg Raises** | 4 min total | 1 round | equipment: none

**Total time:** 17 min

**Why this plan:** selected 4 exercise(s). kept the session to about 17 minute(s). preferred main legs exercises before warmup-like moves. removed exercises that may aggravate the reported pain.

**Safety note:** You reported pain, so this plan stays conservative. Stop if pain gets sharper, spreads, or changes how you move, and consider checking with a clinician if needed.

**Notes:** This output is useful because the planner avoids knee-aggravating exercises while still giving the user a usable workout. A remaining weakness is that pain handling is broad and cannot diagnose injuries.

## Test Case 4: Busy student full-body workout, no equipment, 15 minutes

**User input:**

- Target workout focus: full body
- Available equipment: no equipment
- Workout duration: 15 minutes
- Experience level: beginner
- Busy student / dorm-friendly: checked
- Pain status: no
- Current effort level: 6

**Output:**

1. **Knee Push-Ups** | 5 min total | 1 round | equipment: none
2. **Bodyweight Squats** | 5 min total | 1 round | equipment: none
3. **Shadow Boxing** | 4 min total | 1 round | equipment: none

**Total time:** 14 min

**Why this plan:** selected 3 exercise(s). kept the session to about 14 minute(s). started with upper body, lower body, and core/cardio coverage. leaned on more workout-style moves for the short session. used dorm-friendly options.

**Notes:** This output is useful because the short session includes upper-body, lower-body, and conditioning coverage. A remaining weakness is that the planner still uses simple bucket rules and does not yet build richer circuits or supersets.

## Test Case 5: High effort and pain after a set

**User input:**

- Target workout focus: full body
- Available equipment: no equipment
- Workout duration: 15 minutes
- Experience level: beginner
- Busy student / dorm-friendly: checked
- Pain status: yes
- Pain area: shoulder
- Current effort level: 9

**Output:**

**Next step:** Pause the workout now. Do not push through pain. Rest, breathe, and only switch to very gentle movement if the discomfort clearly settles.

**Safety note:** If the pain is sharp, worsening, or changes normal movement, stop exercising and consider medical guidance.

**Notes:** This is useful because the assistant gives a direct safety-first response instead of encouraging the user to push through pain. A remaining weakness is that it does not yet ask follow-up questions to clarify the type or severity of pain.

## Streamlit Demo Status

The Streamlit app can be run from the repository root with:

```bash
streamlit run mvp/app.py
