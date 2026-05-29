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

LAYOUT_DEPENDENT_GROUPS = {
    ("rule-14.json", "[다만] 그 사이에서 줄이 바뀔 때에는 약자를 사용하여 적는다."),
    ("rule-18.json", "약어를 사용하는 예"),
}

LAYOUT_DEPENDENT_CASES = {
    ("rule-29.json", "그녀는 Los Angeles의 한인 타운에 살고 있다."),
}

DEFERRED_CASES = {
    ("rule-33.json", "우리나라 기차에는 KTX, 새마을호, 무궁화호 등이 있다."),
    ("rule-33.json", "WHO: 세계보건기구"),
    ("rule-33.json", "오동근, 1998a, 1998b; 이진영, 2001, p. 109"),
    ("rule-33.json", "Ms.는 미혼·기혼의 구별이 없는 여성의 존칭이다."),
    ("rule-33.json", "그 영화에서 가장 유명한 곡은 What Is A Youth?이다."),
    ("rule-33.json", "연주가 끝나자 사람들은 Bravo!를 외쳤다."),
    ("rule-33.json", "Summary~연습문제"),
}


def is_supported_case(
    path: Path,
    group_description: str,
    print_text: str,
) -> bool:
    return (
        (path.name, group_description) not in LAYOUT_DEPENDENT_GROUPS
        and (path.name, print_text) not in LAYOUT_DEPENDENT_CASES
        and (path.name, print_text) not in DEFERRED_CASES
    )


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
