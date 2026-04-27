"""Simple rule-based workout planner for the MVP."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "exercises.json"
LEVEL_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}
ROLE_ORDER = {"main": 0, "support": 1, "warmup": 2}
FULL_BODY_BUCKETS = ["upper_body", "lower_body", "core_cardio"]
ROLE_SCORES = {"main": 40, "support": 20, "warmup": 0}
TAG_BONUSES = {
    "bodyweight": 3,
    "compound": 6,
    "conditioning": 5,
    "core": 2,
    "isometric": 1,
    "lower_body": 1,
    "posterior_chain": 2,
    "pull": 3,
    "push": 3,
    "squat": 3,
    "strength": 4,
    "upper_body": 1,
}
TAG_PENALTIES = {
    "balance": -1,
    "low_impact": -2,
    "mobility": -3,
    "stability": -3,
    "warmup": -8,
}


def load_exercises() -> List[Dict[str, Any]]:
    """Load the local JSON dataset."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def matches_equipment(exercise: Dict[str, Any], allowed_equipment: List[str]) -> bool:
    """Return True when the user's available equipment covers the exercise."""
    return set(exercise["equipment"]).issubset(set(allowed_equipment))


def matches_level(exercise: Dict[str, Any], experience_level: str) -> bool:
    """Allow easier exercises for more advanced users, but not the reverse."""
    user_level = LEVEL_ORDER.get(experience_level, 0)
    exercise_level = LEVEL_ORDER.get(exercise["level"], 0)
    return exercise_level <= user_level


def matches_focus(exercise: Dict[str, Any], focus: str) -> bool:
    """Direct focus match, except full-body which can use the whole filtered pool."""
    if focus == "full_body":
        return True
    return exercise["body_part"] == focus


def is_safe_for_pain(exercise: Dict[str, Any], pain_area: Optional[str]) -> bool:
    """Use a conservative filter whenever pain is reported."""
    if pain_area == "knee":
        return not exercise["avoid_if_knee_pain"]
    if pain_area in {"upper_body", "arm", "shoulder", "back"}:
        return not exercise["avoid_if_upper_body_pain"]
    return True


def filter_exercises(
    exercises: List[Dict[str, Any]],
    experience_level: str,
    focus: str,
    equipment: List[str],
    busy_student: bool,
    pain_area: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Apply the base constraint filters."""
    filtered = []

    for exercise in exercises:
        if not matches_level(exercise, experience_level):
            continue
        if not matches_focus(exercise, focus):
            continue
        if not matches_equipment(exercise, equipment):
            continue
        if busy_student and not exercise["dorm_friendly"]:
            continue
        if not is_safe_for_pain(exercise, pain_area):
            continue
        filtered.append(exercise)

    return filtered


def get_full_body_bucket(exercise: Dict[str, Any]) -> str:
    """Group exercises for balanced full-body plans."""
    if exercise["body_part"] in {"arms", "back"}:
        return "upper_body"
    if exercise["body_part"] == "legs":
        return "lower_body"
    return "core_cardio"


def score_exercise(exercise: Dict[str, Any], prefer_conditioning: bool = False) -> int:
    """Score exercises so workout-like moves win over filler and warmups.

    The rules stay intentionally simple:
    - main lifts and conditioning work start ahead
    - strength and bodyweight tags get a boost
    - warmup, mobility, and low-intensity stability work drop down
    - very short full-body sessions can lean toward conditioning finishers
    """
    score = ROLE_SCORES.get(exercise.get("role", "support"), 20)
    tags = set(exercise.get("tags", []))

    for tag in tags:
        score += TAG_BONUSES.get(tag, 0)
        score += TAG_PENALTIES.get(tag, 0)

    if prefer_conditioning and "conditioning" in tags:
        score += 4

    return score


def sort_exercises(
    exercises: List[Dict[str, Any]],
    prefer_conditioning: bool = False,
) -> List[Dict[str, Any]]:
    """Sort exercises by workout quality before falling back to tie-breakers."""
    return sorted(
        exercises,
        key=lambda item: (
            -score_exercise(item, prefer_conditioning=prefer_conditioning),
            ROLE_ORDER.get(item.get("role", "support"), 1),
            -item["estimated_minutes"],
            item["name"],
        ),
    )


def add_exercise(
    summary: Dict[str, Dict[str, Any]],
    ordered_names: List[str],
    exercise: Dict[str, Any],
) -> None:
    """Track minutes and rounds without printing the same exercise as many separate lines."""
    name = exercise["name"]

    if name not in summary:
        summary[name] = {
            "name": name,
            "role": exercise.get("role", "support"),
            "minutes_each": exercise["estimated_minutes"],
            "total_minutes": exercise["estimated_minutes"],
            "body_part": exercise["body_part"],
            "equipment": exercise["equipment"],
            "rounds": 1,
        }
        ordered_names.append(name)
        return

    summary[name]["rounds"] += 1
    summary[name]["total_minutes"] += exercise["estimated_minutes"]


def append_if_fits(
    selected: List[Dict[str, Any]],
    repeat_counts: Dict[str, int],
    exercise: Dict[str, Any],
    used_minutes: int,
    minutes_available: int,
    max_repeats: int,
) -> int:
    """Add an exercise only when it fits the time limit and repeat cap."""
    if repeat_counts.get(exercise["name"], 0) >= max_repeats:
        return used_minutes

    next_total = used_minutes + exercise["estimated_minutes"]
    if next_total > minutes_available:
        return used_minutes

    selected.append(exercise)
    repeat_counts[exercise["name"]] = repeat_counts.get(exercise["name"], 0) + 1
    return next_total


def build_targeted_plan(
    options: List[Dict[str, Any]],
    minutes_available: int,
    max_repeats: int,
) -> List[Dict[str, Any]]:
    """Pick focus-specific exercises, using main moves first and warmups last."""
    selected: List[Dict[str, Any]] = []
    used_minutes = 0
    repeat_counts: Dict[str, int] = {}

    ranked = sort_exercises(options)
    ranked_non_warmup = [
        exercise for exercise in ranked if exercise.get("role", "support") != "warmup"
    ]
    warmups = [exercise for exercise in ranked if exercise.get("role", "support") == "warmup"]

    # First pass: take unique main/support exercises in quality order.
    for exercise in ranked_non_warmup:
        used_minutes = append_if_fits(
            selected,
            repeat_counts,
            exercise,
            used_minutes,
            minutes_available,
            max_repeats,
        )

    if not selected and ranked:
        used_minutes = append_if_fits(
            selected,
            repeat_counts,
            ranked[0],
            used_minutes,
            minutes_available,
            max_repeats,
        )

    # Second pass: allow limited repeats, but still keep warmups at the back of the line.
    while used_minutes < minutes_available and selected:
        added_any = False

        for exercise in ranked_non_warmup:
            new_minutes = append_if_fits(
                selected,
                repeat_counts,
                exercise,
                used_minutes,
                minutes_available,
                max_repeats,
            )
            if new_minutes != used_minutes:
                used_minutes = new_minutes
                added_any = True

        if not added_any:
            break

    # Final pass: only use warmups if time is still left and nothing better fits.
    while used_minutes < minutes_available and warmups:
        added_any = False

        for exercise in warmups:
            new_minutes = append_if_fits(
                selected,
                repeat_counts,
                exercise,
                used_minutes,
                minutes_available,
                max_repeats,
            )
            if new_minutes != used_minutes:
                used_minutes = new_minutes
                added_any = True

        if not added_any:
            break

    return selected


def build_full_body_plan(
    options: List[Dict[str, Any]],
    minutes_available: int,
    max_repeats: int,
) -> List[Dict[str, Any]]:
    """Build a balanced plan with one upper, one lower, and one core/cardio move first."""
    selected: List[Dict[str, Any]] = []
    used_minutes = 0
    repeat_counts: Dict[str, int] = {}
    prefer_conditioning = minutes_available <= 15

    bucketed = {
        bucket: sort_exercises(
            [exercise for exercise in options if get_full_body_bucket(exercise) == bucket],
            prefer_conditioning=prefer_conditioning and bucket == "core_cardio",
        )
        for bucket in FULL_BODY_BUCKETS
    }

    # First pass: try to cover the three full-body buckets with main/support moves first.
    for bucket in FULL_BODY_BUCKETS:
        preferred = [
            exercise
            for exercise in bucketed[bucket]
            if exercise.get("role", "support") != "warmup"
        ]
        fallback = bucketed[bucket]

        for exercise in preferred + [item for item in fallback if item not in preferred]:
            new_minutes = append_if_fits(
                selected,
                repeat_counts,
                exercise,
                used_minutes,
                minutes_available,
                max_repeats,
            )
            if new_minutes != used_minutes:
                used_minutes = new_minutes
                break

    # Second pass: fill time with more main/support work before warmups.
    ranked_non_warmup = sort_exercises(
        [exercise for exercise in options if exercise.get("role", "support") != "warmup"],
        prefer_conditioning=prefer_conditioning,
    )
    while used_minutes < minutes_available and selected:
        added_any = False

        for exercise in ranked_non_warmup:
            new_minutes = append_if_fits(
                selected,
                repeat_counts,
                exercise,
                used_minutes,
                minutes_available,
                max_repeats,
            )
            if new_minutes != used_minutes:
                used_minutes = new_minutes
                added_any = True

        if not added_any:
            break

    # Final pass: only use warmups if time is still left and nothing better fits.
    warmups = sort_exercises(
        [exercise for exercise in options if exercise.get("role", "support") == "warmup"]
    )
    while used_minutes < minutes_available and warmups:
        added_any = False

        for exercise in warmups:
            new_minutes = append_if_fits(
                selected,
                repeat_counts,
                exercise,
                used_minutes,
                minutes_available,
                max_repeats,
            )
            if new_minutes != used_minutes:
                used_minutes = new_minutes
                added_any = True

        if not added_any:
            break

    return selected


def summarize_plan(selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert repeated exercise picks into clean output rows."""
    summary: Dict[str, Dict[str, Any]] = {}
    ordered_names: List[str] = []

    for exercise in selected:
        add_exercise(summary, ordered_names, exercise)

    return [summary[name] for name in ordered_names]


def build_workout_plan(
    experience_level: str,
    focus: str,
    minutes_available: int,
    equipment: List[str],
    busy_student: bool,
    pain_area: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a simple workout plan that respects the main user constraints."""
    exercises = load_exercises()
    options = filter_exercises(
        exercises=exercises,
        experience_level=experience_level,
        focus=focus,
        equipment=equipment,
        busy_student=busy_student,
        pain_area=pain_area,
    )

    max_repeats = 2
    if focus == "full_body":
        selected = build_full_body_plan(options, minutes_available, max_repeats)
    else:
        selected = build_targeted_plan(options, minutes_available, max_repeats)

    summarized_plan = summarize_plan(selected)
    total_minutes = sum(item["total_minutes"] for item in summarized_plan)

    safety_note = None
    if pain_area:
        safety_note = (
            "You reported pain, so this plan stays conservative. Stop if pain gets sharper, "
            "spreads, or changes how you move, and consider checking with a clinician if needed."
        )

    if not summarized_plan:
        return {
            "plan": [],
            "total_minutes": 0,
            "rationale": "No safe workout was found with the current constraints.",
            "safety_note": safety_note,
        }

    rationale_bits = [
        f"selected {len(summarized_plan)} exercise(s)",
        f"kept the session to about {total_minutes} minute(s)",
    ]

    if focus == "full_body":
        rationale_bits.append("started with upper body, lower body, and core/cardio coverage")
        if minutes_available <= 15:
            rationale_bits.append("leaned on more workout-style moves for the short session")
    else:
        rationale_bits.append(
            f"preferred main {focus.replace('_', ' ')} exercises before warmup-like moves"
        )

    if busy_student:
        rationale_bits.append("used dorm-friendly options")
    if pain_area:
        rationale_bits.append("removed exercises that may aggravate the reported pain")

    return {
        "plan": summarized_plan,
        "total_minutes": total_minutes,
        "rationale": ". ".join(rationale_bits) + ".",
        "safety_note": safety_note,
    }


def next_step_for_effort_and_pain(high_effort: bool, pain_reported: bool) -> Dict[str, str]:
    """Return a conservative coaching response for an in-the-moment check-in."""
    if pain_reported:
        return {
            "message": (
                "Pause the workout now. Do not push through pain. Rest, breathe, and only switch "
                "to very gentle movement if the discomfort clearly settles."
            ),
            "safety_note": (
                "If the pain is sharp, worsening, or changes normal movement, stop exercising and "
                "consider medical guidance."
            ),
        }

    if high_effort:
        return {
            "message": (
                "Take a longer rest, lower the intensity for the next set, and focus on clean form "
                "before you continue."
            ),
            "safety_note": "Stop early if high effort turns into pain, dizziness, or poor form.",
        }

    return {
        "message": "You can continue with your next set if your breathing and form both feel steady.",
        "safety_note": "Check in with your form before continuing.",
    }
