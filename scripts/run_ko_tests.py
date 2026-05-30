#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from braille import ascii_to_dots, dots_to_ascii, dots_to_unicode
from hangul import inkprint_to_braille_dots
from hangul.tests.test_support import jamo_role_for_case


def iter_cases(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in data["groups"]:
        for inkprint_text, expected in group["tests"].items():
            yield group["description"], inkprint_text, expected


def trim_blank_edges(cells: list[str]) -> list[str]:
    start = 0
    end = len(cells)
    while start < end and cells[start] == "":
        start += 1
    while end > start and cells[end - 1] == "":
        end -= 1
    return cells[start:end]


def run(path: Path) -> int:
    failures = []
    total = 0

    for group_description, inkprint_text, expected in iter_cases(path):
        total += 1
        try:
            actual_dots = inkprint_to_braille_dots(
                inkprint_text,
                jamo_role=jamo_role_for_case(path, group_description),
            )
            actual_ascii = dots_to_ascii(actual_dots)
            actual_unicode = dots_to_unicode(actual_dots)
        except Exception as exc:
            failures.append(
                (group_description, inkprint_text, expected, None, None, str(exc))
            )
            continue

        expected_dots = trim_blank_edges(ascii_to_dots(expected["ascii"]))
        comparable_actual_dots = trim_blank_edges(actual_dots)
        comparable_actual_unicode = dots_to_unicode(comparable_actual_dots)
        expected_unicode = dots_to_unicode(expected_dots)
        if (
            comparable_actual_dots != expected_dots
            or comparable_actual_unicode != expected_unicode
        ):
            failures.append(
                (
                    group_description,
                    inkprint_text,
                    expected,
                    actual_ascii,
                    actual_unicode,
                    None,
                )
            )

    for (
        group_description,
        inkprint_text,
        expected,
        actual_ascii,
        actual_unicode,
        error,
    ) in failures:
        print(f"FAIL {path.name} / {group_description} / {inkprint_text}")
        if error:
            print(f"  error:    {error}")
        print(f"  expected: {expected['ascii']} / {expected['unicode']}")
        if actual_ascii is not None:
            print(f"  actual:   {actual_ascii} / {actual_unicode}")

    passed = total - len(failures)
    print(f"{path.name}: {passed}/{total} passed")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rule", type=int, default=1)
    args = parser.parse_args()

    path = ROOT / "src" / "hangul" / "rules" / "cases" / f"rule-{args.rule}.json"
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main())
