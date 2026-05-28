from pathlib import Path

SUPPORTED_RULES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def standalone_jamo_for_case(path: Path, group_description: str) -> str:
    if path.name in {"rule-3.json", "rule-5.json"} and (
        "받침으로 쓰일 때" in group_description or group_description == "겹받침"
    ):
        return "jongseong"
    if path.name in {"rule-8.json", "rule-9.json"}:
        return "standalone"
    if path.name == "rule-10.json":
        return "attached_jongseong"
    return "choseong"
