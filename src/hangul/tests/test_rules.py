import json
from pathlib import Path

import pytest

from braille import ascii_to_dots, dots_to_unicode
from hangul import print_to_braille_dots
from hangul.tests.test_support import (
    SUPPORTED_RULES,
    is_supported_case,
    jamo_role_for_case,
)

HANGUL_ROOT = Path(__file__).resolve().parent.parent
RULE_CASES_ROOT = HANGUL_ROOT / "rules" / "cases"


def iter_rule_cases(rule: int):
    path = RULE_CASES_ROOT / f"rule-{rule}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in data["groups"]:
        for print_text, expected in group["tests"].items():
            yield path, group["description"], print_text, expected


def trim_blank_edges(cells: list[str]) -> list[str]:
    start = 0
    end = len(cells)
    while start < end and cells[start] == "":
        start += 1
    while end > start and cells[end - 1] == "":
        end -= 1
    return cells[start:end]


@pytest.mark.parametrize(
    ("path", "group_description", "print_text", "expected"),
    [
        case
        for rule in SUPPORTED_RULES
        for case in iter_rule_cases(rule)
        if is_supported_case(case[0], case[1], case[2])
    ],
)
def test_supported_ko_rules(path, group_description, print_text, expected):
    actual_dots = print_to_braille_dots(
        print_text,
        jamo_role=jamo_role_for_case(path, group_description),
    )

    actual_dots = trim_blank_edges(actual_dots)
    expected_dots = trim_blank_edges(ascii_to_dots(expected["ascii"]))

    assert actual_dots == expected_dots
    assert dots_to_unicode(actual_dots) == dots_to_unicode(expected_dots)
