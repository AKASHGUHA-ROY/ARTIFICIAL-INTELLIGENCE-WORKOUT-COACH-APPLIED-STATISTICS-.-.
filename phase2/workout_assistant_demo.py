#!/usr/bin/env python3
"""
Workout Assistant Demo

This script reads baseline and improved workout-assistant outputs from Markdown
files and prints a simple comparison report for all test cases.

Expected files in the same folder:
- baseline_outputs.md
- improved_outputs.md

Optional:
- README.md (not used by this script)

Run:
    python workout_assistant_demo.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parent
BASELINE_FILE = BASE_DIR / "artifacts" / "baseline_outputs.md"
IMPROVED_FILE = BASE_DIR / "artifacts" / "improved_outputs.md"


@dataclass
class TestCase:
    case_id: int
    user_input: str
    baseline_text: str = ""
    improved_text: str = ""


TEST_CASES: List[TestCase] = [
    TestCase(
        case_id=1,
        user_input="Beginner user, ARM day, no equipment, 20 minutes.",
    ),
    TestCase(
        case_id=2,
        user_input="Intermediate user, back day, dumbbells only, 45 minutes.",
    ),
    TestCase(
        case_id=3,
        user_input="Beginner user, leg day, knee pain reported.",
    ),
    TestCase(
        case_id=4,
        user_input="Busy student, full body workout, 15 minutes.",
    ),
    TestCase(
        case_id=5,
        user_input="User reports high effort and pain after a set and asks what to do next.",
    ),
]


def read_text_file(path: Path) -> str:
    """Read a text file if it exists; otherwise return an empty string."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_section(md_text: str, case_id: int) -> str:
    """
    Extract the section under '## Test Case X' until the next '## Test Case Y'
    or the end of the document.
    """
    if not md_text.strip():
        return ""

    pattern = rf"^##\s+Test Case\s+{case_id}\s*$"
    match = re.search(pattern, md_text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""

    start = match.end()

    next_match = re.search(
        r"^##\s+Test Case\s+\d+\s*$",
        md_text[start:],
        flags=re.IGNORECASE | re.MULTILINE,
    )

    if next_match:
        end = start + next_match.start()
    else:
        end = len(md_text)

    section = md_text[start:end].strip()
    return section


def normalize_whitespace(text: str) -> str:
    """Clean up extra whitespace for nicer display."""
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines).strip()


def load_test_case_texts() -> None:
    """Populate each test case with baseline and improved text from markdown files."""
    baseline_md = read_text_file(BASELINE_FILE)
    improved_md = read_text_file(IMPROVED_FILE)

    for tc in TEST_CASES:
        tc.baseline_text = extract_section(baseline_md, tc.case_id)
        tc.improved_text = extract_section(improved_md, tc.case_id)


def count_words(text: str) -> int:
    """Approximate word count."""
    words = re.findall(r"\b\S+\b", text)
    return len(words)


def count_bullets(text: str) -> int:
    """Count bullet lines in a section."""
    return sum(
        1
        for line in text.splitlines()
        if line.lstrip().startswith("- ") or line.lstrip().startswith("* ")
    )


def score_response(text: str) -> Dict[str, int]:
    """
    Simple heuristic scoring rubric for a workout-assistant response.
    Scores range from 1 to 5.
    """
    lower = text.lower()

    personalization = 3
    safety = 3
    constraint_handling = 3
    brevity = 3
    actionability = 3

    # Personalization
    if any(term in lower for term in ["beginner", "intermediate", "busy", "student", "no equipment", "dumbbells only", "knee"]):
        personalization += 1
    if any(term in lower for term in ["20 minutes", "45 minutes", "15 minutes"]):
        personalization += 1

    # Safety
    if any(term in lower for term in ["stop", "pain", "red flag", "sharp pain", "medical", "doctor", "clinician", "physiotherapist"]):
        safety += 1
    if "push through" in lower or "ignore pain" in lower:
        safety -= 2

    # Constraint handling
    if any(term in lower for term in ["no equipment", "dumbbells only", "busy", "dorm", "small space", "shared space"]):
        constraint_handling += 1
    if any(term in lower for term in ["15 minutes", "20 minutes", "45 minutes"]):
        constraint_handling += 1

    # Brevity
    word_count = count_words(text)
    if word_count <= 120:
        brevity += 2
    elif word_count <= 180:
        brevity += 1
    elif word_count > 350:
        brevity -= 1

    # Actionability
    if any(term in lower for term in ["do this", "next step", "try", "switch", "rest", "reduce", "stop", "use"]):
        actionability += 1
    if count_bullets(text) > 0:
        actionability += 1

    return {
        "personalization": max(1, min(5, personalization)),
        "safety": max(1, min(5, safety)),
        "constraint_handling": max(1, min(5, constraint_handling)),
        "brevity": max(1, min(5, brevity)),
        "actionability": max(1, min(5, actionability)),
    }


def avg_score(scores: Dict[str, int]) -> float:
    return round(sum(scores.values()) / len(scores), 2)


def print_block(title: str, content: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if content.strip():
        print(normalize_whitespace(content))
    else:
        print("[Not found]")


def print_case_report(tc: TestCase) -> None:
    print("=" * 80)
    print(f"TEST CASE {tc.case_id}")
    print("=" * 80)
    print(f"User input: {tc.user_input}")

    print_block("Baseline output", tc.baseline_text)
    baseline_scores = score_response(tc.baseline_text)
    print("Baseline scores:", baseline_scores, "Average:", avg_score(baseline_scores))

    print_block("Improved output", tc.improved_text)
    improved_scores = score_response(tc.improved_text)
    print("Improved scores:", improved_scores, "Average:", avg_score(improved_scores))

    delta = round(avg_score(improved_scores) - avg_score(baseline_scores), 2)
    print(f"Overall change: {delta:+.2f}")


def print_summary(test_cases: List[TestCase]) -> None:
    print("\n" + "#" * 80)
    print("SUMMARY")
    print("#" * 80)

    rows: List[Tuple[int, float, float, float]] = []
    for tc in test_cases:
        b = avg_score(score_response(tc.baseline_text))
        i = avg_score(score_response(tc.improved_text))
        rows.append((tc.case_id, b, i, round(i - b, 2)))

    print(f"{'Case':<6}{'Baseline':<12}{'Improved':<12}{'Change':<10}")
    print("-" * 40)
    for case_id, baseline_avg, improved_avg, change in rows:
        print(f"{case_id:<6}{baseline_avg:<12}{improved_avg:<12}{change:+.2f}")

    overall_baseline = round(sum(r[1] for r in rows) / len(rows), 2) if rows else 0.0
    overall_improved = round(sum(r[2] for r in rows) / len(rows), 2) if rows else 0.0
    overall_change = round(overall_improved - overall_baseline, 2)

    print("-" * 40)
    print(f"{'AVG':<6}{overall_baseline:<12}{overall_improved:<12}{overall_change:+.2f}")


def main() -> None:
    load_test_case_texts()

    missing_baseline = not BASELINE_FILE.exists()
    missing_improved = not IMPROVED_FILE.exists()

    if missing_baseline:
        print(f"Warning: {BASELINE_FILE.name} not found.")
    if missing_improved:
        print(f"Warning: {IMPROVED_FILE.name} not found.")

    for tc in TEST_CASES:
        print_case_report(tc)

    print_summary(TEST_CASES)


if __name__ == "__main__":
    main()
