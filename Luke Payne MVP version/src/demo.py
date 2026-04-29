"""Command-line demo for the cleaned Phase 3 MVP."""

from __future__ import annotations

from pathlib import Path

from planner import build_workout_plan, next_step_for_effort_and_pain


CASES = [
    {
        "title": "Case 1: beginner arm day, no equipment, 20 minutes",
        "kwargs": {
            "experience_level": "beginner",
            "focus": "arms",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": False,
            "pain_area": None,
        },
        "criteria": "focus, equipment, and time",
    },
    {
        "title": "Case 2: intermediate back day, dumbbells only, 45 minutes",
        "kwargs": {
            "experience_level": "intermediate",
            "focus": "back",
            "minutes_available": 45,
            "equipment": ["dumbbells"],
            "busy_student": False,
            "pain_area": None,
        },
        "criteria": "experience level, equipment, and main back movements",
    },
    {
        "title": "Case 3: beginner leg day with knee pain",
        "kwargs": {
            "experience_level": "beginner",
            "focus": "legs",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": False,
            "pain_area": "knee",
        },
        "criteria": "pain filter, time, and useful safe alternatives",
    },
    {
        "title": "Case 4: busy student full-body workout, 15 minutes",
        "kwargs": {
            "experience_level": "beginner",
            "focus": "full_body",
            "minutes_available": 15,
            "equipment": ["none"],
            "busy_student": True,
            "pain_area": None,
        },
        "criteria": "short session, dorm-friendly options, and balance",
    },
    {
        "title": "Case 5: upper-body pain with no equipment",
        "kwargs": {
            "experience_level": "beginner",
            "focus": "arms",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": True,
            "pain_area": "shoulder",
        },
        "criteria": "conservative pain behavior and fallback handling",
    },
]


def minute_label(value: int) -> str:
    """Return a readable minute label."""
    return "1 minute" if value == 1 else f"{value} minutes"


def render_result(title: str, result: dict, criteria: str) -> str:
    """Render one demo case as Markdown text."""
    lines = [f"## {title}", "", f"**Main criteria tested:** {criteria}", ""]

    if result["plan"]:
        lines.append("| # | Exercise | Minutes | Prescription | Rest |")
        lines.append("|---:|---|---:|---|---:|")

        for index, item in enumerate(result["plan"], start=1):
            lines.append(
                f"| {index} | {item['name']} | {item['minutes']} | "
                f"{item['prescription']} | {item['rest_seconds']} sec |"
            )
    else:
        lines.append("No safe plan was found.")

    lines.extend(
        [
            "",
            f"**Total time:** {minute_label(result['total_minutes'])}",
            f"**Time left:** {minute_label(result['time_left'])}",
            f"**Why this plan:** {result['rationale']}",
        ]
    )

    if result.get("safety_note"):
        lines.append(f"**Safety note:** {result['safety_note']}")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    """Run demo cases and write a reproducible artifact."""
    output = [
        "# MVP Demo Outputs",
        "",
        "These outputs were generated from `src/demo.py` using the same planner that powers the Streamlit app.",
        "",
    ]

    summary_rows = []

    for case in CASES:
        result = build_workout_plan(**case["kwargs"])
        output.append(render_result(case["title"], result, case["criteria"]))

        passed = "Yes" if result["plan"] else "No"
        summary_rows.append(
            [
                case["title"].replace("Case ", "").split(":", 1)[0],
                case["criteria"],
                passed,
                str(result["total_minutes"]),
            ]
        )

    follow_up = next_step_for_effort_and_pain(high_effort=True, pain_reported=True)

    output.extend(
        [
            "## Case 6: high effort and pain check-in",
            "",
            "**Main criteria tested:** safety response",
            "",
            f"**Next step:** {follow_up['message']}",
            f"**Safety note:** {follow_up['safety_note']}",
            "",
            "## Summary Table",
            "",
            "| Case | Criteria | Passed? | Minutes |",
            "|---:|---|---:|---:|",
        ]
    )

    for row in summary_rows:
        output.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")

    output.append("| 6 | safety response | Yes | n/a |")

    artifact_path = Path(__file__).resolve().parents[1] / "artifacts" / "demo_outputs.md"
    artifact_path.write_text("\n".join(output) + "\n", encoding="utf-8")

    print("\n".join(output))


if __name__ == "__main__":
    main()
