from pathlib import Path

SUPPORTED_RULES = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    28,
    29,
    30,
    31,
    32,
    33,
    35,
    36,
    37,
    40,
]

LINE_AWARE_CASES = {
    ("rule-14.json", "철수는 여름 방학을 맞아 바위섬으로 놀러 갔다."): (32, 2),
    ("rule-29.json", "그녀는 Los Angeles의 한인 타운에 살고 있다."): (32, 2),
}


def is_supported_case(
    path: Path,
    group_description: str,
    inkprint_text: str,
) -> bool:
    return True


def line_width_for_case(path: Path, inkprint_text: str) -> int | None:
    layout = LINE_AWARE_CASES.get((path.name, inkprint_text))
    if layout is None:
        return None
    return layout[0]


def initial_line_position_for_case(path: Path, inkprint_text: str) -> int:
    layout = LINE_AWARE_CASES.get((path.name, inkprint_text))
    if layout is None:
        return 0
    return layout[1]


def jamo_role_for_case(path: Path, group_description: str) -> str:
    if path.name == "rule-36.json" and group_description == "로마 숫자":
        return "roman_numeral"
    if path.name in {"rule-3.json", "rule-5.json"} and (
        "받침으로 쓰일 때" in group_description or group_description == "겹받침"
    ):
        return "t"
    if path.name in {"rule-8.json", "rule-9.json"}:
        return "standalone"
    if path.name == "rule-10.json":
        return "attached_t"
    return "l"
