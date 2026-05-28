#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from braille import ascii_to_dots, dots_to_ascii, dots_to_unicode
from hangul import print_to_braille_dots


def iter_cases(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in data["groups"]:
        for print_text, expected in group["tests"].items():
            yield group["description"], print_text, expected


def standalone_jamo_for_case(path: Path, group_description: str) -> str:
    if path.name in {"rule-3.json", "rule-5.json"} and (
        "받침으로 쓰일 때" in group_description or "겹받침" == group_description
    ):
        return "jongseong"
    return "choseong"


def run(path: Path) -> int:
    failures = []
    total = 0

    for group_description, print_text, expected in iter_cases(path):
        total += 1
        try:
            actual_dots = print_to_braille_dots(
                print_text,
                standalone_jamo=standalone_jamo_for_case(path, group_description),
            )
            actual_ascii = dots_to_ascii(actual_dots)
            actual_unicode = dots_to_unicode(actual_dots)
        except Exception as exc:
            failures.append((group_description, print_text, expected, None, None, str(exc)))
            continue

        expected_dots = ascii_to_dots(expected["ascii"])
        if actual_dots != expected_dots or actual_unicode != expected["unicode"]:
            failures.append(
                (group_description, print_text, expected, actual_ascii, actual_unicode, None)
            )

    for group_description, print_text, expected, actual_ascii, actual_unicode, error in failures:
        print(f"FAIL {path.name} / {group_description} / {print_text}")
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

    path = ROOT / "tests" / "ko" / f"rule-{args.rule}.json"
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main())
