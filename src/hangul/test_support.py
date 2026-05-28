from pathlib import Path

SUPPORTED_RULES = [1, 2, 3, 4, 5, 6, 7]


def standalone_jamo_for_case(path: Path, group_description: str) -> str:
    if path.name in {"rule-3.json", "rule-5.json"} and (
        "받침으로 쓰일 때" in group_description or group_description == "겹받침"
    ):
        return "jongseong"
    return "choseong"
