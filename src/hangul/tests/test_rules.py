import json
from pathlib import Path

import pytest

from braille import ascii_to_dots, dots_to_unicode
from hangul import inkprint_to_braille_dots
from hangul.tests.test_support import (
    SUPPORTED_RULES,
    initial_line_position_for_case,
    is_supported_case,
    jamo_role_for_case,
    line_width_for_case,
)

HANGUL_ROOT = Path(__file__).resolve().parent.parent
RULE_CASES_ROOT = HANGUL_ROOT / "rules" / "cases"


def iter_rule_cases(rule: int):
    path = RULE_CASES_ROOT / f"rule-{rule}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in data["groups"]:
        for inkprint_text, expected in group["tests"].items():
            yield path, group["description"], inkprint_text, expected


def trim_blank_edges(cells: list[str]) -> list[str]:
    start = 0
    end = len(cells)
    while start < end and cells[start] == "":
        start += 1
    while end > start and cells[end - 1] == "":
        end -= 1
    return cells[start:end]


def expected_ascii_variants(ascii_text: str) -> list[str]:
    lines = ascii_text.splitlines()
    if len(lines) == 1:
        return [ascii_text]

    variants = [lines[0]]
    for line in lines[1:]:
        next_variants = []
        for prefix in variants:
            padding_removed = prefix.rstrip("`")
            next_variants.append(prefix + line)
            next_variants.append(padding_removed + line)
            next_variants.append(padding_removed + "`" + line)
        variants = next_variants
    return list(dict.fromkeys(variants))


def expected_ascii_to_dots(ascii_text: str) -> list[list[str]]:
    return [
        trim_blank_edges(ascii_to_dots(variant))
        for variant in expected_ascii_variants(ascii_text)
    ]


@pytest.mark.parametrize(
    ("path", "group_description", "inkprint_text", "expected"),
    [
        case
        for rule in SUPPORTED_RULES
        for case in iter_rule_cases(rule)
        if is_supported_case(case[0], case[1], case[2])
    ],
)
def test_supported_ko_rules(path, group_description, inkprint_text, expected):
    actual_dots = inkprint_to_braille_dots(
        inkprint_text,
        jamo_role=jamo_role_for_case(path, group_description),
        line_width=line_width_for_case(path, inkprint_text),
        initial_line_position=initial_line_position_for_case(path, inkprint_text),
    )

    actual_dots = trim_blank_edges(actual_dots)
    expected_dots_variants = expected_ascii_to_dots(expected["ascii"])

    assert actual_dots in expected_dots_variants
    assert any(
        dots_to_unicode(actual_dots) == dots_to_unicode(expected_dots)
        for expected_dots in expected_dots_variants
    )
