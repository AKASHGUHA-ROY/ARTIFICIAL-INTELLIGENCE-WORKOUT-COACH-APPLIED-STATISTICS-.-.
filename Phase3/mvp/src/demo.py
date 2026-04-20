"""Run the sample MVP workout-planner cases."""

from __future__ import annotations

import sys
from pathlib import Path


# Make local imports work cleanly when running: python3 mvp/src/demo.py
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from planner import build_workout_plan, next_step_for_effort_and_pain


def print_divider() -> None:
    """Print a simple divider between cases."""
    print("-" * 60)


def print_case(title: str, result: dict) -> None:
    """Pretty-print one workout result."""
    print(title)
    print_divider()

    if result["plan"]:
        for index, item in enumerate(result["plan"], start=1):
            equipment_text = ", ".join(item["equipment"])
            rounds_text = f"{item['rounds']} round(s)" if item["rounds"] > 1 else "1 round"
            print(
                f"{index}. {item['name']} | {item['total_minutes']} min total | "
                f"{rounds_text} | equipment: {equipment_text}"
            )
    else:
        print("No plan available.")

    print(f"Total time: {result['total_minutes']} min")
    print(f"Why this plan: {result['rationale']}")

    if result.get("safety_note"):
        print(f"Safety note: {result['safety_note']}")

    print()


def main() -> None:
    """Run the five requested benchmark scenarios."""
    cases = [
        (
            "Case 1: beginner arm day, no equipment, 20 minutes",
            build_workout_plan(
                experience_level="beginner",
                focus="arms",
                minutes_available=20,
                equipment=["none"],
                busy_student=False,
            ),
        ),
        (
            "Case 2: intermediate back day, dumbbells only, 45 minutes",
            build_workout_plan(
                experience_level="intermediate",
                focus="back",
                minutes_available=45,
                equipment=["dumbbells"],
                busy_student=False,
            ),
        ),
        (
            "Case 3: beginner leg day with knee pain",
            build_workout_plan(
                experience_level="beginner",
                focus="legs",
                minutes_available=20,
                equipment=["none"],
                busy_student=False,
                pain_area="knee",
            ),
        ),
        (
            "Case 4: busy student full-body workout, 15 minutes",
            build_workout_plan(
                experience_level="beginner",
                focus="full_body",
                minutes_available=15,
                equipment=["none"],
                busy_student=True,
            ),
        ),
    ]

    for title, result in cases:
        print_case(title, result)

    follow_up = next_step_for_effort_and_pain(high_effort=True, pain_reported=True)
    print("Case 5: user reports high effort and pain after a set")
    print_divider()
    print(f"Next step: {follow_up['message']}")
    print(f"Safety note: {follow_up['safety_note']}")


if __name__ == "__main__":
    main()
