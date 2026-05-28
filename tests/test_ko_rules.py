import json
from pathlib import Path

import pytest

from braille import ascii_to_dots, dots_to_unicode
from hangul import print_to_braille_dots

ROOT = Path(__file__).resolve().parents[1]


def iter_rule_cases(rule: int):
    path = ROOT / "tests" / "ko" / f"rule-{rule}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in data["groups"]:
        for print_text, expected in group["tests"].items():
            yield path, group["description"], print_text, expected


def standalone_jamo_for_case(path: Path, group_description: str) -> str:
    if path.name in {"rule-3.json", "rule-5.json"} and (
        "받침으로 쓰일 때" in group_description or "겹받침" == group_description
    ):
        return "jongseong"
    return "choseong"


@pytest.mark.parametrize(
    ("path", "group_description", "print_text", "expected"),
    [
        case
        for rule in [1, 2, 3, 4, 5, 6]
        for case in iter_rule_cases(rule)
    ],
)
def test_ko_rules_1_to_4(path, group_description, print_text, expected):
    actual_dots = print_to_braille_dots(
        print_text,
        standalone_jamo=standalone_jamo_for_case(path, group_description),
    )

    assert actual_dots == ascii_to_dots(expected["ascii"])
    assert dots_to_unicode(actual_dots) == expected["unicode"]
