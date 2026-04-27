# Improved Demo Outputs

This file records the current benchmark-style outputs from the MVP workout planner. These examples are based on the finalized demo behavior in `src/demo.py`.

## Test Case 1

**User input:** Beginner arm day, no equipment, 20 minutes.

**Improved output:**

1. **Close-Grip Knee Push-Ups** | 5 min total | 1 round | equipment: none
2. **Knee Push-Ups** | 5 min total | 1 round | equipment: none
3. **Wall Push-Ups** | 4 min total | 1 round | equipment: none
4. **Triceps Press-Backs** | 2 min total | 1 round | equipment: none
5. **Shoulder Taps** | 4 min total | 1 round | equipment: none

**Total time:** 20 min  
**Why this plan:** selected 5 exercise(s). kept the session to about 20 minute(s). preferred main arms exercises before warmup-like moves.

**Notes:** Better than the baseline because the workout now starts with more demanding main exercises and has enough no-equipment arm options to fill the 20-minute target. Remaining weakness: the planner still does not assign sets, reps, or rest periods.

## Test Case 2

**User input:** Intermediate back day, dumbbells only, 45 minutes.

**Improved output:**

1. **Renegade Rows** | 6 min total | 1 round | equipment: dumbbells
2. **Chest-Supported Dumbbell Rows** | 8 min total | 1 round | equipment: dumbbells
3. **Bent-Over Dumbbell Rows** | 7 min total | 1 round | equipment: dumbbells
4. **Single-Arm Dumbbell Rows** | 7 min total | 1 round | equipment: dumbbells
5. **Dumbbell Pullovers** | 7 min total | 1 round | equipment: dumbbells
6. **Rear Delt Raises** | 6 min total | 1 round | equipment: dumbbells
7. **Dumbbell Shrugs** | 4 min total | 1 round | equipment: dumbbells

**Total time:** 45 min  
**Why this plan:** selected 7 exercise(s). kept the session to about 45 minute(s). preferred main back exercises before warmup-like moves.

**Notes:** Better than the baseline because larger rowing movements are clearly prioritized before support work, and the dumbbell-only back pool is large enough to fill the requested time. Remaining weakness: the planner still does not assign sets, reps, or rest periods, so the output is closer to exercise selection than a full coaching plan.

## Test Case 3

**User input:** Beginner leg day, 20 minutes, with knee pain.

**Improved output:**

1. **Glute Bridges** | 5 min total | 1 round | equipment: none
2. **Standing Hip Extensions** | 3 min total | 1 round | equipment: none
3. **Standing Calf Raises** | 4 min total | 1 round | equipment: none
4. **Clamshells** | 4 min total | 1 round | equipment: none
5. **Side-Lying Leg Raises** | 4 min total | 1 round | equipment: none

**Total time:** 20 min  
**Why this plan:** selected 5 exercise(s). kept the session to about 20 minute(s). preferred main legs exercises before warmup-like moves. removed exercises that may aggravate the reported pain.  
**Safety note:** You reported pain, so this plan stays conservative. Stop if pain gets sharper, spreads, or changes how you move, and consider checking with a clinician if needed.

**Notes:** Better than the baseline because the plan stays conservative, excludes knee-aggravating options, and still fills the 20-minute target. Remaining weakness: the pain handling is broad and cannot personalize for severity, diagnosis, or rehab needs.

## Test Case 4

**User input:** Busy student full-body workout, no equipment, 15 minutes.

**Improved output:**

1. **Close-Grip Knee Push-Ups** | 5 min total | 1 round | equipment: none
2. **Bodyweight Squats** | 5 min total | 1 round | equipment: none
3. **Standing Cross-Body Crunches** | 5 min total | 1 round | equipment: none

**Total time:** 15 min  
**Why this plan:** selected 3 exercise(s). kept the session to about 15 minute(s). started with upper body, lower body, and core/cardio coverage. leaned on more workout-style moves for the short session. used dorm-friendly options.

**Notes:** Better than the baseline because the short session fills the requested time with clear upper-body, lower-body, and core/cardio coverage. Remaining weakness: the planner still uses simple bucket rules and cannot yet build richer short circuits or supersets.

## Test Case 5

**User input:** User reports high effort and pain after a set.

**Improved output:**

**Next step:** Pause the workout now. Do not push through pain. Rest, breathe, and only switch to very gentle movement if the discomfort clearly settles.  
**Safety note:** If the pain is sharp, worsening, or changes normal movement, stop exercising and consider medical guidance.

**Notes:** Better than a generic motivational response because it is direct, conservative, and safety-first. Remaining weakness: it is still a simple rule-based message and does not ask follow-up questions to clarify the kind of pain.
