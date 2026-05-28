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


def rule_1_choseong_dot(choseong: str) -> Optional[str]:
    return RULE_1_CHOSEONG_DOT.get(choseong)


def rule_2_tense_choseong_dots(choseong: str) -> Optional[list[str]]:
    return RULE_2_TENSE_CHOSEONG_DOTS.get(choseong)


def rule_3_jongseong_dot(jongseong: str) -> Optional[str]:
    return RULE_3_JONGSEONG_DOT.get(jongseong)


def rule_4_double_jongseong_dots(jongseong: str) -> Optional[list[str]]:
    return RULE_4_DOUBLE_JONGSEONG_DOTS.get(jongseong)


def rule_5_composite_jongseong_dots(jongseong: str) -> Optional[list[str]]:
    return RULE_5_COMPOSITE_JONGSEONG_DOTS.get(jongseong)


def rule_6_jungseong_dot(jungseong: str) -> Optional[str]:
    return RULE_6_JUNGSEONG_DOT.get(jungseong)


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

    tense_dots = rule_2_tense_choseong_dots(choseong)
    if tense_dots is not None:
        return tense_dots

    dot = rule_1_choseong_dot(choseong)
    if dot is not None:
        return [dot]

    raise NotImplementedError(f"unsupported choseong: {choseong}")


def encode_jungseong(jungseong: str) -> list[str]:
    dot = rule_6_jungseong_dot(jungseong)
    if dot is not None:
        return [dot]

    raise NotImplementedError(f"unsupported jungseong: {jungseong}")


def encode_jongseong(jongseong: str) -> list[str]:
    if not jongseong:
        return []

    double_dots = rule_4_double_jongseong_dots(jongseong)
    if double_dots is not None:
        return double_dots

    composite_dots = rule_5_composite_jongseong_dots(jongseong)
    if composite_dots is not None:
        return composite_dots

    dot = rule_3_jongseong_dot(jongseong)
    if dot is not None:
        return [dot]

    raise NotImplementedError(f"unsupported jongseong: {jongseong}")


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
    tense_dots = rule_2_tense_choseong_dots(ch)
    if tense_dots is not None:
        return tense_dots

    if role == "jongseong":
        return encode_jongseong(ch)

    choseong_dot = rule_1_choseong_dot(ch)
    if choseong_dot is not None:
        return [choseong_dot]

    jungseong_dot = rule_6_jungseong_dot(ch)
    if jungseong_dot is not None:
        return [jungseong_dot]

    raise NotImplementedError(f"unsupported character: {ch}")
