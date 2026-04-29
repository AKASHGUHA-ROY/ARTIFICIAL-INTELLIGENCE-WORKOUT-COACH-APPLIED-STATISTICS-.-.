"""Rule-based workout planner for the MAE 301 MVP.

The goal is to keep the logic easy to inspect for grading. The planner does not
claim to diagnose injuries or replace a trainer. It uses a small local exercise
dataset, user constraints, and clear scoring rules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "exercises.json"

LEVEL_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}
ROLE_ORDER = {"main": 0, "support": 1, "warmup": 2}
FULL_BODY_BUCKETS = ["upper_body", "lower_body", "core_cardio"]

ROLE_SCORES = {"main": 50, "support": 25, "warmup": 5}

TAG_BONUSES = {
    "bodyweight": 4,
    "compound": 8,
    "conditioning": 6,
    "core": 5,
    "glutes": 4,
    "hamstrings": 4,
    "lats": 4,
    "lower_body": 4,
    "posterior_chain": 5,
    "pull": 5,
    "push": 5,
    "squat": 4,
    "strength": 7,
    "upper_body": 4,
}

TAG_PENALTIES = {
    "balance": -1,
    "mobility": -2,
    "stability": -1,
    "warmup": -10,
}


def load_exercises() -> List[Dict[str, Any]]:
    """Load the local JSON exercise dataset."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_focus(focus: str) -> str:
    """Normalize the focus value used by the app and command-line demo."""
    focus = focus.lower().strip().replace(" ", "_")
    allowed = {"arms", "back", "legs", "core", "full_body"}
    if focus not in allowed:
        return "full_body"
    return focus


def normalize_equipment(equipment: List[str]) -> List[str]:
    """Remove duplicate equipment values while keeping simple safe defaults."""
    clean = []
    for item in equipment:
        item = item.lower().strip()
        if item not in clean:
            clean.append(item)

    if not clean:
        clean = ["none"]

    return clean


def matches_equipment(exercise: Dict[str, Any], allowed_equipment: List[str]) -> bool:
    """Return True when the user has all equipment required for the exercise."""
    return set(exercise["equipment"]).issubset(set(allowed_equipment))


def matches_level(exercise: Dict[str, Any], experience_level: str) -> bool:
    """Allow easier exercises for more experienced users, but not the reverse."""
    user_level = LEVEL_ORDER.get(experience_level, 0)
    exercise_level = LEVEL_ORDER.get(exercise["level"], 0)
    return exercise_level <= user_level


def matches_focus(exercise: Dict[str, Any], focus: str) -> bool:
    """Match a targeted focus, or allow all categories for full-body plans."""
    if focus == "full_body":
        return True
    return exercise["body_part"] == focus


def is_safe_for_pain(exercise: Dict[str, Any], pain_area: Optional[str]) -> bool:
    """Use conservative safety filters when pain is reported."""
    if pain_area == "knee":
        return not exercise.get("avoid_if_knee_pain", False)

    if pain_area in {"upper_body", "arm", "shoulder", "back", "elbow", "wrist"}:
        return not exercise.get("avoid_if_upper_body_pain", False)

    return True


def get_bucket(exercise: Dict[str, Any]) -> str:
    """Group exercises for balanced full-body plans."""
    body_part = exercise["body_part"]

    if body_part in {"arms", "back"}:
        return "upper_body"

    if body_part == "legs":
        return "lower_body"

    return "core_cardio"


def score_exercise(exercise: Dict[str, Any], focus: str, minutes_available: int) -> int:
    """Score an exercise so useful main movements beat filler movements."""
    tags = set(exercise.get("tags", []))
    score = ROLE_SCORES.get(exercise.get("role", "support"), 20)

    for tag in tags:
        score += TAG_BONUSES.get(tag, 0)
        score += TAG_PENALTIES.get(tag, 0)

    if exercise["body_part"] == focus:
        score += 12

    if focus == "full_body" and exercise["body_part"] == "full_body":
        score += 10

    if minutes_available <= 15 and "conditioning" in tags:
        score += 5

    if minutes_available <= 15 and exercise["estimated_minutes"] <= 5:
        score += 3

    return score


def sort_options(
    options: List[Dict[str, Any]],
    focus: str,
    minutes_available: int,
) -> List[Dict[str, Any]]:
    """Sort available exercises from most useful to least useful."""
    return sorted(
        options,
        key=lambda item: (
            -score_exercise(item, focus, minutes_available),
            ROLE_ORDER.get(item.get("role", "support"), 1),
            item["estimated_minutes"],
            item["name"],
        ),
    )


def filter_exercises(
    exercises: List[Dict[str, Any]],
    experience_level: str,
    focus: str,
    equipment: List[str],
    busy_student: bool,
    pain_area: Optional[str],
) -> List[Dict[str, Any]]:
    """Apply user constraints before ranking exercises."""
    filtered = []

    for exercise in exercises:
        if not matches_level(exercise, experience_level):
            continue

        if not matches_focus(exercise, focus):
            continue

        if not matches_equipment(exercise, equipment):
            continue

        if busy_student and not exercise.get("dorm_friendly", False):
            continue

        if not is_safe_for_pain(exercise, pain_area):
            continue

        filtered.append(exercise)

    return filtered


def pick_targeted_plan(
    options: List[Dict[str, Any]],
    focus: str,
    minutes_available: int,
) -> List[Dict[str, Any]]:
    """Choose a targeted workout within the user's time limit."""
    ranked = sort_options(options, focus, minutes_available)
    selected = []
    used_minutes = 0

    non_warmups = [item for item in ranked if item.get("role") != "warmup"]
    warmups = [item for item in ranked if item.get("role") == "warmup"]

    for exercise in non_warmups + warmups:
        next_total = used_minutes + exercise["estimated_minutes"]
        if next_total <= minutes_available:
            selected.append(exercise)
            used_minutes = next_total

    if not selected and ranked:
        selected.append(ranked[0])

    return selected


def pick_full_body_plan(
    options: List[Dict[str, Any]],
    minutes_available: int,
) -> List[Dict[str, Any]]:
    """Choose a balanced full-body workout within the user's time limit."""
    selected = []
    used_minutes = 0

    for bucket in FULL_BODY_BUCKETS:
        bucket_options = [item for item in options if get_bucket(item) == bucket]
        ranked = sort_options(bucket_options, "full_body", minutes_available)

        for exercise in ranked:
            next_total = used_minutes + exercise["estimated_minutes"]
            if next_total <= minutes_available:
                selected.append(exercise)
                used_minutes = next_total
                break

    remaining = [item for item in options if item not in selected]
    ranked_remaining = sort_options(remaining, "full_body", minutes_available)

    for exercise in ranked_remaining:
        next_total = used_minutes + exercise["estimated_minutes"]
        if next_total <= minutes_available:
            selected.append(exercise)
            used_minutes = next_total

    if not selected and ranked_remaining:
        selected.append(ranked_remaining[0])

    return selected


def get_prescription(exercise: Dict[str, Any], experience_level: str) -> str:
    """Create a simple sets and reps style instruction."""
    tags = set(exercise.get("tags", []))
    role = exercise.get("role", "support")

    if role == "warmup":
        return "1 easy round for 2 to 3 minutes"

    if "isometric" in tags:
        return "2 to 3 holds of 20 to 30 seconds"

    if "cardio" in tags or "conditioning" in tags:
        return "2 to 3 rounds of 30 to 45 seconds"

    if "dumbbells" in exercise.get("equipment", []):
        if experience_level == "beginner":
            return "2 sets of 8 to 10 controlled reps"
        return "3 sets of 8 to 12 controlled reps"

    if exercise["body_part"] == "core":
        return "2 to 3 sets of 8 to 12 slow reps"

    return "2 to 3 sets of 8 to 15 controlled reps"


def get_rest_seconds(exercise: Dict[str, Any]) -> int:
    """Recommend a simple rest period."""
    if exercise.get("role") == "main":
        return 60
    if exercise.get("role") == "warmup":
        return 20
    return 45


def get_form_cue(exercise: Dict[str, Any]) -> str:
    """Return one simple form cue for the exercise."""
    tags = set(exercise.get("tags", []))

    if "push" in tags:
        return "Keep your body tight and stop the set if your shoulders feel sharp pain."

    if "pull" in tags or "lats" in tags:
        return "Pull with control and avoid shrugging your shoulders up."

    if "squat" in tags:
        return "Move slowly and keep your knees tracking in line with your toes."

    if "core" in tags:
        return "Brace your stomach and keep your lower back from arching."

    if "glutes" in tags or "posterior_chain" in tags:
        return "Squeeze the glutes and keep the motion controlled."

    if "cardio" in tags or "conditioning" in tags:
        return "Keep the pace steady enough that you can control your breathing."

    return "Use a controlled pace and stop if the movement feels painful."


def format_plan(
    selected: List[Dict[str, Any]],
    experience_level: str,
) -> List[Dict[str, Any]]:
    """Convert selected exercises into readable plan rows."""
    plan = []

    for exercise in selected:
        plan.append(
            {
                "name": exercise["name"],
                "body_part": exercise["body_part"],
                "role": exercise.get("role", "support"),
                "equipment": ", ".join(exercise.get("equipment", [])),
                "minutes": exercise["estimated_minutes"],
                "prescription": get_prescription(exercise, experience_level),
                "rest_seconds": get_rest_seconds(exercise),
                "form_cue": get_form_cue(exercise),
            }
        )

    return plan


def build_safety_note(pain_area: Optional[str]) -> Optional[str]:
    """Create a conservative pain note when pain is reported."""
    if not pain_area:
        return None

    return (
        "Pain was reported, so the planner removed exercises that may aggravate that area. "
        "This is not medical advice. Stop if pain gets sharper, spreads, or changes how you move."
    )


def build_rationale(
    plan: List[Dict[str, Any]],
    focus: str,
    total_minutes: int,
    minutes_available: int,
    busy_student: bool,
    pain_area: Optional[str],
    fallback_used: bool,
) -> str:
    """Explain why the plan was selected."""
    reasons = [
        f"Selected {len(plan)} exercise(s)",
        f"kept the plan at {total_minutes} minutes out of {minutes_available} available minutes",
    ]

    if focus == "full_body":
        reasons.append("balanced upper body, lower body, and core or conditioning work")
    else:
        reasons.append(f"prioritized the requested {focus.replace('_', ' ')} focus")

    if busy_student:
        reasons.append("kept the plan dorm-friendly")

    if pain_area:
        reasons.append("used conservative pain filters")

    if fallback_used:
        reasons.append("used a safe fallback because the exact request had limited matches")

    return ". ".join(reasons) + "."


def build_workout_plan(
    experience_level: str,
    focus: str,
    minutes_available: int,
    equipment: List[str],
    busy_student: bool,
    pain_area: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a personalized workout plan from simple user constraints."""
    focus = normalize_focus(focus)
    equipment = normalize_equipment(equipment)
    minutes_available = max(5, min(int(minutes_available), 75))

    exercises = load_exercises()
    options = filter_exercises(
        exercises=exercises,
        experience_level=experience_level,
        focus=focus,
        equipment=equipment,
        busy_student=busy_student,
        pain_area=pain_area,
    )

    fallback_used = False

    if not options and focus != "full_body":
        fallback_used = True
        options = filter_exercises(
            exercises=exercises,
            experience_level=experience_level,
            focus="full_body",
            equipment=equipment,
            busy_student=busy_student,
            pain_area=pain_area,
        )

    if focus == "full_body":
        selected = pick_full_body_plan(options, minutes_available)
    else:
        selected = pick_targeted_plan(options, focus, minutes_available)

    plan = format_plan(selected, experience_level)
    total_minutes = sum(item["minutes"] for item in plan)

    if not plan:
        return {
            "plan": [],
            "total_minutes": 0,
            "time_left": minutes_available,
            "rationale": "No safe plan was found with the current constraints.",
            "safety_note": build_safety_note(pain_area),
            "metadata": {
                "focus": focus,
                "equipment": equipment,
                "fallback_used": fallback_used,
                "candidate_count": 0,
            },
        }

    return {
        "plan": plan,
        "total_minutes": total_minutes,
        "time_left": max(0, minutes_available - total_minutes),
        "rationale": build_rationale(
            plan=plan,
            focus=focus,
            total_minutes=total_minutes,
            minutes_available=minutes_available,
            busy_student=busy_student,
            pain_area=pain_area,
            fallback_used=fallback_used,
        ),
        "safety_note": build_safety_note(pain_area),
        "metadata": {
            "focus": focus,
            "equipment": equipment,
            "fallback_used": fallback_used,
            "candidate_count": len(options),
        },
    }


def next_step_for_effort_and_pain(
    high_effort: bool,
    pain_reported: bool,
) -> Dict[str, str]:
    """Return a conservative next-step coaching response."""
    if pain_reported:
        return {
            "message": (
                "Pause the workout now. Do not push through pain. Rest and only return to very "
                "easy movement if the discomfort clearly settles."
            ),
            "safety_note": (
                "If pain is sharp, worsening, spreading, or changing normal movement, stop the "
                "workout and consider medical guidance."
            ),
        }

    if high_effort:
        return {
            "message": (
                "Take a longer rest, lower the next set slightly, and focus on clean form before "
                "continuing."
            ),
            "safety_note": "Stop early if high effort turns into pain, dizziness, or poor form.",
        }

    return {
        "message": "Continue if your breathing is controlled and your form still feels steady.",
        "safety_note": "Check your form before the next set.",
    }
