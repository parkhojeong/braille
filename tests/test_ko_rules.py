import json
from pathlib import Path

import pytest

from braille import ascii_to_dots, dots_to_unicode
from hangul import print_to_braille_dots
from hangul.test_support import SUPPORTED_RULES, standalone_jamo_for_case

ROOT = Path(__file__).resolve().parents[1]


def iter_rule_cases(rule: int):
    path = ROOT / "tests" / "ko" / f"rule-{rule}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in data["groups"]:
        for print_text, expected in group["tests"].items():
            yield path, group["description"], print_text, expected


@pytest.mark.parametrize(
    ("path", "group_description", "print_text", "expected"),
    [
        case
        for rule in SUPPORTED_RULES
        for case in iter_rule_cases(rule)
    ],
)
def test_supported_ko_rules(path, group_description, print_text, expected):
    actual_dots = print_to_braille_dots(
        print_text,
        standalone_jamo=standalone_jamo_for_case(path, group_description),
    )

    assert actual_dots == ascii_to_dots(expected["ascii"])
    assert dots_to_unicode(actual_dots) == expected["unicode"]
