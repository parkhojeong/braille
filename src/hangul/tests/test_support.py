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
]

UNSUPPORTED_LAYOUT_GROUPS = {
    ("rule-14.json", "[다만] 그 사이에서 줄이 바뀔 때에는 약자를 사용하여 적는다."),
    ("rule-18.json", "약어를 사용하는 예"),
    ("rule-28.json", "[붙임] 대문자 표기 예"),
}


def is_supported_case(path: Path, group_description: str) -> bool:
    return (path.name, group_description) not in UNSUPPORTED_LAYOUT_GROUPS


def jamo_role_for_case(path: Path, group_description: str) -> str:
    if path.name in {"rule-3.json", "rule-5.json"} and (
        "받침으로 쓰일 때" in group_description or group_description == "겹받침"
    ):
        return "t"
    if path.name in {"rule-8.json", "rule-9.json"}:
        return "standalone"
    if path.name == "rule-10.json":
        return "attached_t"
    return "l"
