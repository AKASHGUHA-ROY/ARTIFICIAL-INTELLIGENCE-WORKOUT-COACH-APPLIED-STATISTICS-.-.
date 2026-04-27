"""Interactive terminal demo for the MVP workout planner."""

from __future__ import annotations

import sys
from pathlib import Path


# Make local imports work cleanly when running: python3 src/chat_demo.py
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from planner import build_workout_plan


VALID_LEVELS = ["beginner", "intermediate", "advanced"]
VALID_FOCUSES = ["arms", "back", "legs", "core", "full_body"]


def normalize_answer(value: str) -> str:
    """Normalize simple terminal answers into planner-friendly values."""
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def prompt_choice(prompt: str, choices: list[str]) -> str:
    """Ask until the user enters one of the allowed values."""
    choices_text = ", ".join(choices)

    while True:
        answer = normalize_answer(input(f"{prompt} ({choices_text}): "))
        if answer in choices:
            return answer

        print(f"Please enter one of: {choices_text}")


def prompt_minutes() -> int:
    """Ask for a positive whole-number time limit."""
    while True:
        answer = input("Minutes available: ").strip()

        try:
            minutes = int(answer)
        except ValueError:
            print("Please enter a whole number, like 15 or 30.")
            continue

        if minutes > 0:
            return minutes

        print("Please enter a number greater than 0.")


def prompt_equipment() -> list[str]:
    """Ask for comma-separated equipment names."""
    answer = input("Equipment available (example: none, dumbbells, chair): ").strip()
    if not answer:
        return ["none"]

    equipment = [
        normalize_answer(item)
        for item in answer.split(",")
        if normalize_answer(item)
    ]

    return equipment or ["none"]


def prompt_yes_no(prompt: str) -> bool:
    """Ask a yes/no question."""
    while True:
        answer = normalize_answer(input(f"{prompt} (yes/no): "))
        if answer in {"yes", "y"}:
            return True
        if answer in {"no", "n"}:
            return False

        print("Please enter yes or no.")


def prompt_optional_pain_area() -> str | None:
    """Ask for an optional pain area to filter around."""
    answer = normalize_answer(
        input("Pain area to avoid? Press Enter for none (examples: knee, shoulder, back): ")
    )

    if answer in {"", "none", "no", "n/a"}:
        return None

    return answer


def print_workout(result: dict) -> None:
    """Print the planner result in a clear terminal format."""
    print()
    print("Your workout plan")
    print("-" * 60)

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


def main() -> None:
    """Collect user inputs and print a generated workout plan."""
    print("MVP Workout Planner")
    print("Answer a few questions to get a simple workout plan.")
    print()

    experience_level = prompt_choice("Experience level", VALID_LEVELS)
    focus = prompt_choice("Workout focus", VALID_FOCUSES)
    minutes_available = prompt_minutes()
    equipment = prompt_equipment()
    busy_student = prompt_yes_no("Are you a busy student who needs dorm-friendly options?")
    pain_area = prompt_optional_pain_area()

    result = build_workout_plan(
        experience_level=experience_level,
        focus=focus,
        minutes_available=minutes_available,
        equipment=equipment,
        busy_student=busy_student,
        pain_area=pain_area,
    )

    print_workout(result)


if __name__ == "__main__":
    main()
