from typing import Callable, Optional


RULE_1_CHOSEONG_DOT = {
    "ㄱ": "4",
    "ㄴ": "14",
    "ㄷ": "24",
    "ㄹ": "5",
    "ㅁ": "15",
    "ㅂ": "45",
    "ㅅ": "6",
    "ㅇ": "1245",
    "ㅈ": "46",
    "ㅊ": "56",
    "ㅋ": "124",
    "ㅌ": "125",
    "ㅍ": "145",
    "ㅎ": "245",
}

RULE_2_TENSE_CHOSEONG_DOTS = {
    "ㄲ": ["6", RULE_1_CHOSEONG_DOT["ㄱ"]],
    "ㄸ": ["6", RULE_1_CHOSEONG_DOT["ㄷ"]],
    "ㅃ": ["6", RULE_1_CHOSEONG_DOT["ㅂ"]],
    "ㅆ": ["6", RULE_1_CHOSEONG_DOT["ㅅ"]],
    "ㅉ": ["6", RULE_1_CHOSEONG_DOT["ㅈ"]],
}

RULE_6_JUNGSEONG_DOT = {
    "ㅏ": "126",
    "ㅑ": "345",
    "ㅓ": "234",
    "ㅕ": "156",
    "ㅗ": "136",
    "ㅛ": "346",
    "ㅜ": "134",
    "ㅠ": "146",
    "ㅡ": "246",
    "ㅚ": "13456",
    "ㅣ": "135",
}

RULE_3_JONGSEONG_DOT = {
    "ㄱ": "1",
    "ㄴ": "25",
    "ㄷ": "35",
    "ㄹ": "2",
    "ㅁ": "26",
    "ㅂ": "12",
    "ㅅ": "3",
    "ㅇ": "2356",
    "ㅈ": "13",
    "ㅊ": "23",
    "ㅋ": "235",
    "ㅌ": "236",
    "ㅍ": "256",
    "ㅎ": "356",
    "ㅆ": "34",
}

RULE_4_DOUBLE_JONGSEONG_DOTS = {
    "ㄲ": [RULE_3_JONGSEONG_DOT["ㄱ"], RULE_3_JONGSEONG_DOT["ㄱ"]],
    "ㅆ": [RULE_3_JONGSEONG_DOT["ㅆ"]],
}

RULE_5_COMPOSITE_JONGSEONG_DOTS = {
    "ㄳ": [RULE_3_JONGSEONG_DOT["ㄱ"], RULE_3_JONGSEONG_DOT["ㅅ"]],
    "ㄵ": [RULE_3_JONGSEONG_DOT["ㄴ"], RULE_3_JONGSEONG_DOT["ㅈ"]],
    "ㄶ": [RULE_3_JONGSEONG_DOT["ㄴ"], RULE_3_JONGSEONG_DOT["ㅎ"]],
    "ㄺ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㄱ"]],
    "ㄻ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㅁ"]],
    "ㄼ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㅂ"]],
    "ㄽ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㅅ"]],
    "ㄾ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㅌ"]],
    "ㄿ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㅍ"]],
    "ㅀ": [RULE_3_JONGSEONG_DOT["ㄹ"], RULE_3_JONGSEONG_DOT["ㅎ"]],
    "ㅄ": [RULE_3_JONGSEONG_DOT["ㅂ"], RULE_3_JONGSEONG_DOT["ㅅ"]],
}


def lookup(mapping: dict[str, str], key: str, label: str) -> str:
    try:
        return mapping[key]
    except KeyError:
        raise NotImplementedError(f"unsupported {label}: {key}") from None


def rule_1_choseong_dot(choseong: str) -> str:
    return lookup(RULE_1_CHOSEONG_DOT, choseong, "choseong")


def apply_rule_2_tense_choseong(choseong: str) -> Optional[list[str]]:
    return RULE_2_TENSE_CHOSEONG_DOTS.get(choseong)


def rule_3_jongseong_dot(jongseong: str) -> str:
    return lookup(RULE_3_JONGSEONG_DOT, jongseong, "jongseong")


def apply_rule_4_double_jongseong(jongseong: str) -> Optional[list[str]]:
    return RULE_4_DOUBLE_JONGSEONG_DOTS.get(jongseong)


def apply_rule_5_composite_jongseong(jongseong: str) -> Optional[list[str]]:
    return RULE_5_COMPOSITE_JONGSEONG_DOTS.get(jongseong)


def rule_6_jungseong_dot(jungseong: str) -> str:
    return lookup(RULE_6_JUNGSEONG_DOT, jungseong, "jungseong")


def apply_abbreviated_a_syllable_rule(
    choseong: str,
    jungseong: str,
    jongseong: str,
) -> Optional[list[str]]:
    if jungseong == "ㅏ":
        if choseong == "ㅅ":
            return ["123", *encode_jongseong(jongseong)]
        if choseong in {"ㄷ", "ㅌ", "ㅎ"}:
            return [RULE_1_CHOSEONG_DOT[choseong], *encode_jongseong(jongseong)]

    return None


def encode_choseong(choseong: str) -> list[str]:
    if choseong == "ㅇ":
        return []

    tense_dots = apply_rule_2_tense_choseong(choseong)
    if tense_dots is not None:
        return tense_dots

    return [rule_1_choseong_dot(choseong)]


def encode_jungseong(jungseong: str) -> list[str]:
    return [rule_6_jungseong_dot(jungseong)]


def encode_jongseong(jongseong: str) -> list[str]:
    if not jongseong:
        return []

    double_dots = apply_rule_4_double_jongseong(jongseong)
    if double_dots is not None:
        return double_dots

    composite_dots = apply_rule_5_composite_jongseong(jongseong)
    if composite_dots is not None:
        return composite_dots

    return [rule_3_jongseong_dot(jongseong)]


SyllableRule = Callable[[str, str, str], Optional[list[str]]]

SYLLABLE_RULES: list[SyllableRule] = [
    apply_abbreviated_a_syllable_rule,
]


def encode_syllable(choseong: str, jungseong: str, jongseong: str) -> list[str]:
    for rule in SYLLABLE_RULES:
        result = rule(choseong, jungseong, jongseong)
        if result is not None:
            return result

    return [
        *encode_choseong(choseong),
        *encode_jungseong(jungseong),
        *encode_jongseong(jongseong),
    ]


def encode_standalone_jamo(ch: str, role: str) -> list[str]:
    tense_dots = apply_rule_2_tense_choseong(ch)
    if tense_dots is not None:
        return tense_dots

    if role == "jongseong":
        return encode_jongseong(ch)

    if ch in RULE_1_CHOSEONG_DOT:
        return [rule_1_choseong_dot(ch)]

    if ch in RULE_6_JUNGSEONG_DOT:
        return [rule_6_jungseong_dot(ch)]

    raise NotImplementedError(f"unsupported standalone jamo: {ch}")
