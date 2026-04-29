# MVP Demo Outputs

These outputs were generated from `src/demo.py` using the same planner that powers the Streamlit app.

## Case 1: beginner arm day, no equipment, 20 minutes

**Main criteria tested:** focus, equipment, and time

| # | Exercise | Minutes | Prescription | Rest |
|---:|---|---:|---|---:|
| 1 | Knee Push-Ups | 5 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 2 | Wall Push-Ups | 4 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 3 | Shoulder Taps | 4 | 2 to 3 sets of 8 to 15 controlled reps | 45 sec |
| 4 | Arm Circles | 3 | 1 easy round for 2 to 3 minutes | 20 sec |

**Total time:** 16 minutes
**Time left:** 4 minutes
**Why this plan:** Selected 4 exercise(s). kept the plan at 16 minutes out of 20 available minutes. prioritized the requested arms focus.

## Case 2: intermediate back day, dumbbells only, 45 minutes

**Main criteria tested:** experience level, equipment, and main back movements

| # | Exercise | Minutes | Prescription | Rest |
|---:|---|---:|---|---:|
| 1 | Bent-Over Dumbbell Rows | 7 | 3 sets of 8 to 12 controlled reps | 60 sec |
| 2 | Single-Arm Dumbbell Rows | 7 | 3 sets of 8 to 12 controlled reps | 60 sec |
| 3 | Chest-Supported Dumbbell Rows | 8 | 3 sets of 8 to 12 controlled reps | 60 sec |
| 4 | Dumbbell Pullovers | 7 | 3 sets of 8 to 12 controlled reps | 60 sec |
| 5 | Rear Delt Raises | 6 | 3 sets of 8 to 12 controlled reps | 45 sec |
| 6 | Dumbbell Reverse Fly | 6 | 3 sets of 8 to 12 controlled reps | 45 sec |

**Total time:** 41 minutes
**Time left:** 4 minutes
**Why this plan:** Selected 6 exercise(s). kept the plan at 41 minutes out of 45 available minutes. prioritized the requested back focus.

## Case 3: beginner leg day with knee pain

**Main criteria tested:** pain filter, time, and useful safe alternatives

| # | Exercise | Minutes | Prescription | Rest |
|---:|---|---:|---|---:|
| 1 | Glute Bridges | 5 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 2 | Clamshells | 4 | 2 to 3 sets of 8 to 15 controlled reps | 45 sec |
| 3 | Side-Lying Leg Raises | 4 | 2 to 3 sets of 8 to 15 controlled reps | 45 sec |
| 4 | Standing Calf Raises | 4 | 2 to 3 sets of 8 to 15 controlled reps | 45 sec |

**Total time:** 17 minutes
**Time left:** 3 minutes
**Why this plan:** Selected 4 exercise(s). kept the plan at 17 minutes out of 20 available minutes. prioritized the requested legs focus. used conservative pain filters.
**Safety note:** Pain was reported, so the planner removed exercises that may aggravate that area. This is not medical advice. Stop if pain gets sharper, spreads, or changes how you move.

## Case 4: busy student full-body workout, 15 minutes

**Main criteria tested:** short session, dorm-friendly options, and balance

| # | Exercise | Minutes | Prescription | Rest |
|---:|---|---:|---|---:|
| 1 | Knee Push-Ups | 5 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 2 | Bodyweight Squats | 5 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 3 | Shadow Boxing | 4 | 2 to 3 rounds of 30 to 45 seconds | 60 sec |

**Total time:** 14 minutes
**Time left:** 1 minute
**Why this plan:** Selected 3 exercise(s). kept the plan at 14 minutes out of 15 available minutes. balanced upper body, lower body, and core or conditioning work. kept the plan dorm-friendly.

## Case 5: upper-body pain with no equipment

**Main criteria tested:** conservative pain behavior and fallback handling

| # | Exercise | Minutes | Prescription | Rest |
|---:|---|---:|---|---:|
| 1 | Bodyweight Squats | 5 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 2 | Glute Bridges | 5 | 2 to 3 sets of 8 to 15 controlled reps | 60 sec |
| 3 | Bird Dog | 4 | 2 to 3 sets of 8 to 12 slow reps | 60 sec |
| 4 | Dead Bug | 4 | 2 to 3 sets of 8 to 12 slow reps | 60 sec |

**Total time:** 18 minutes
**Time left:** 2 minutes
**Why this plan:** Selected 4 exercise(s). kept the plan at 18 minutes out of 20 available minutes. prioritized the requested arms focus. kept the plan dorm-friendly. used conservative pain filters. used a safe fallback because the exact request had limited matches.
**Safety note:** Pain was reported, so the planner removed exercises that may aggravate that area. This is not medical advice. Stop if pain gets sharper, spreads, or changes how you move.

## Case 6: high effort and pain check-in

**Main criteria tested:** safety response

**Next step:** Pause the workout now. Do not push through pain. Rest and only return to very easy movement if the discomfort clearly settles.
**Safety note:** If pain is sharp, worsening, spreading, or changing normal movement, stop the workout and consider medical guidance.

## Summary Table

| Case | Criteria | Passed? | Minutes |
|---:|---|---:|---:|
| 1 | focus, equipment, and time | Yes | 16 |
| 2 | experience level, equipment, and main back movements | Yes | 41 |
| 3 | pain filter, time, and useful safe alternatives | Yes | 17 |
| 4 | short session, dorm-friendly options, and balance | Yes | 14 |
| 5 | conservative pain behavior and fallback handling | Yes | 18 |
| 6 | safety response | Yes | n/a |
