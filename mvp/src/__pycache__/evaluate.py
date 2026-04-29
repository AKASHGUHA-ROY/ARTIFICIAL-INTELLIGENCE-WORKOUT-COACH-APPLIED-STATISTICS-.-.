"""Evaluate the MVP workout planner across realistic user scenarios."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
ARTIFACTS_DIR = PROJECT_DIR / "artifacts"
RESULTS_PATH = ARTIFACTS_DIR / "evaluation_results.md"

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from planner import build_workout_plan, load_exercises, next_step_for_effort_and_pain


Scenario = Dict[str, Any]
EvaluationRecord = Dict[str, Any]


SCENARIOS: List[Scenario] = [
    {
        "name": "beginner arms, no equipment, 20 minutes",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "arms",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": False,
        },
    },
    {
        "name": "intermediate back, dumbbells only, 45 minutes",
        "type": "plan",
        "inputs": {
            "experience_level": "intermediate",
            "focus": "back",
            "minutes_available": 45,
            "equipment": ["dumbbells"],
            "busy_student": False,
        },
    },
    {
        "name": "beginner legs with knee pain",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "legs",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": False,
            "pain_area": "knee",
        },
    },
    {
        "name": "busy student full-body, no equipment, 15 minutes",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "full_body",
            "minutes_available": 15,
            "equipment": ["none"],
            "busy_student": True,
        },
    },
    {
        "name": "high effort with pain",
        "type": "coaching",
        "inputs": {
            "high_effort": True,
            "pain_reported": True,
        },
    },
    {
        "name": "missed workout with only 10 minutes",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "full_body",
            "minutes_available": 10,
            "equipment": ["none"],
            "busy_student": False,
        },
    },
    {
        "name": "shoulder/upper body pain",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "full_body",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": False,
            "pain_area": "shoulder",
        },
    },
    {
        "name": "dorm/quiet workout (no jumping)",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "full_body",
            "minutes_available": 20,
            "equipment": ["none"],
            "busy_student": True,
        },
    },
    {
        "name": "very short 5-minute workout",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "core",
            "minutes_available": 5,
            "equipment": ["none"],
            "busy_student": False,
        },
    },
    {
        "name": "edge case: no valid exercises available",
        "type": "plan",
        "inputs": {
            "experience_level": "beginner",
            "focus": "back",
            "minutes_available": 15,
            "equipment": ["none"],
            "busy_student": False,
            "pain_area": "shoulder",
        },
    },
]


def exercise_lookup() -> Dict[str, Dict[str, Any]]:
    """Return exercises keyed by name for metadata-based checks."""
    return {exercise["name"]: exercise for exercise in load_exercises()}


def run_scenario(scenario: Scenario) -> Dict[str, Any]:
    """Call the planner or coaching helper for one scenario."""
    inputs = scenario["inputs"]

    if scenario["type"] == "plan":
        return build_workout_plan(**inputs)

    if scenario["type"] == "coaching":
        return next_step_for_effort_and_pain(**inputs)

    raise ValueError(f"Unknown scenario type: {scenario['type']}")


def get_plan_items(output: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract a plan list from the planner output."""
    plan = output.get("plan", [])
    return plan if isinstance(plan, list) else []


def get_total_minutes(output: Dict[str, Any]) -> int:
    """Read total minutes from output, falling back to plan item totals."""
    total = output.get("total_minutes")

    if isinstance(total, int):
        return total

    return sum(
        int(item.get("total_minutes", item.get("estimated_minutes", 0)))
        for item in get_plan_items(output)
    )


def get_catalog_item(
    plan_item: Dict[str, Any],
    catalog: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Prefer full catalog metadata, but fall back to the plan item."""
    return catalog.get(plan_item.get("name", ""), plan_item)


def exercise_is_safe_for_pain(
    exercise: Dict[str, Any],
    pain_area: Optional[str],
) -> bool:
    """Apply the same conservative pain categories used by the planner."""
    if pain_area == "knee":
        return not exercise.get("avoid_if_knee_pain", False)

    if pain_area in {"upper_body", "arm", "shoulder", "back"}:
        return not exercise.get("avoid_if_upper_body_pain", False)

    return True


def evaluate_plan(
    output: Dict[str, Any],
    inputs: Dict[str, Any],
    catalog: Dict[str, Dict[str, Any]],
) -> Dict[str, bool]:
    """Evaluate planner output against simple rule-based checks."""
    plan_items = get_plan_items(output)
    total_minutes = get_total_minutes(output)
    allowed_equipment = set(inputs.get("equipment", []))
    focus = inputs.get("focus")
    pain_area = inputs.get("pain_area")

    return {
        "time_ok": total_minutes <= inputs.get("minutes_available", 0),
        "equipment_ok": all(
            set(item.get("equipment", [])).issubset(allowed_equipment)
            for item in plan_items
        ),
        "pain_safe": all(
            exercise_is_safe_for_pain(get_catalog_item(item, catalog), pain_area)
            for item in plan_items
        ),
        "focus_match": all(
            focus == "full_body"
            or get_catalog_item(item, catalog).get("body_part") == focus
            for item in plan_items
        ),
        "plan_exists": bool(plan_items),
    }


def evaluate_coaching(output: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, bool]:
    """Evaluate coaching output for safety-aware language when pain is reported."""
    response_text = " ".join(
        str(output.get(key, "")) for key in ("message", "safety_note")
    ).lower()
    safety_words = ("stop", "pause", "reduce", "lower", "rest", "gentle")

    return {
        "safety_response": (
            not inputs.get("pain_reported", False)
            or any(word in response_text for word in safety_words)
        )
    }


def summarize_plan_output(output: Dict[str, Any]) -> str:
    """Create a compact human-readable summary for plan outputs."""
    plan_items = get_plan_items(output)

    if not plan_items:
        return (
            "No plan returned. "
            f"Total minutes: {get_total_minutes(output)}. "
            f"Rationale: {output.get('rationale', 'No rationale provided.')}"
        )

    exercise_bits = []

    for item in plan_items:
        equipment_text = ", ".join(item.get("equipment", [])) or "unspecified"
        exercise_bits.append(
            f"{item.get('name', 'Unknown exercise')} "
            f"({item.get('total_minutes', '?')} min, equipment: {equipment_text})"
        )

    return (
        f"Total minutes: {get_total_minutes(output)}. "
        f"Exercises: {'; '.join(exercise_bits)}. "
        f"Rationale: {output.get('rationale', 'No rationale provided.')}"
    )


def summarize_coaching_output(output: Dict[str, Any]) -> str:
    """Create a compact summary for coaching outputs."""
    return (
        f"Message: {output.get('message', '')} "
        f"Safety note: {output.get('safety_note', '')}"
    ).strip()


def summarize_output(scenario: Scenario, output: Dict[str, Any]) -> str:
    """Create the correct summary for the scenario type."""
    if scenario["type"] == "plan":
        return summarize_plan_output(output)

    return summarize_coaching_output(output)


def evaluate_scenario(
    scenario: Scenario,
    output: Dict[str, Any],
    catalog: Dict[str, Dict[str, Any]],
) -> Dict[str, bool]:
    """Run the correct checks for the scenario type."""
    if scenario["type"] == "plan":
        return evaluate_plan(output, scenario["inputs"], catalog)

    return evaluate_coaching(output, scenario["inputs"])


def status_text(passed: bool) -> str:
    """Render a boolean check result."""
    return "PASS" if passed else "FAIL"


def build_evaluation_records() -> List[EvaluationRecord]:
    """Run every scenario and collect inputs, outputs, and check results."""
    catalog = exercise_lookup()
    records = []

    for scenario in SCENARIOS:
        output = run_scenario(scenario)
        checks = evaluate_scenario(scenario, output, catalog)

        records.append(
            {
                "name": scenario["name"],
                "type": scenario["type"],
                "inputs": scenario["inputs"],
                "output": output,
                "output_summary": summarize_output(scenario, output),
                "checks": checks,
                "passed": all(checks.values()),
            }
        )

    return records


def print_records(records: List[EvaluationRecord]) -> None:
    """Print a readable terminal report."""
    total_passed = sum(1 for record in records if record["passed"])

    print("Evaluation Results")
    print("=" * 60)
    print(f"Total scenarios: {len(records)}")
    print(f"Passed: {total_passed}")
    print()

    for record in records:
        print(f"Scenario: {record['name']}")
        print(f"Type: {record['type']}")
        print(f"Overall: {status_text(record['passed'])}")
        print("Checks:")

        for check_name, passed in record["checks"].items():
            print(f"  - {check_name}: {status_text(passed)}")

        print(f"Output: {record['output_summary']}")
        print("-" * 60)


def write_markdown(records: List[EvaluationRecord]) -> None:
    """Write the evaluation report to artifacts/evaluation_results.md."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    total_passed = sum(1 for record in records if record["passed"])
    lines = [
        "# Evaluation Results",
        "",
        "## Summary",
        f"- Total scenarios: {len(records)}",
        f"- Passed: {total_passed}",
        "",
        "## Scenario Results",
        "",
    ]

    for record in records:
        lines.extend(
            [
                f"### Scenario: {record['name']}",
                "Inputs:",
                "```json",
                json.dumps(record["inputs"], indent=2, sort_keys=True),
                "```",
                "",
                "Output:",
                record["output_summary"],
                "",
                "Checks:",
            ]
        )

        for check_name, passed in record["checks"].items():
            lines.append(f"- {check_name}: {status_text(passed)}")

        lines.append("")

    RESULTS_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run evaluations, print them, and write a markdown artifact."""
    records = build_evaluation_records()
    print_records(records)
    write_markdown(records)
    print(f"Markdown results written to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
