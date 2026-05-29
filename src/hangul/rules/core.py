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

RULE_7_JUNGSEONG_DOTS = {
    "ㅐ": ["1235"],
    "ㅒ": [RULE_6_JUNGSEONG_DOT["ㅑ"], "1235"],
    "ㅔ": ["1345"],
    "ㅖ": ["34"],
    "ㅘ": ["1236"],
    "ㅙ": ["1236", "1235"],
    "ㅚ": ["13456"],
    "ㅝ": ["1234"],
    "ㅞ": ["1234", "1235"],
    "ㅟ": [RULE_6_JUNGSEONG_DOT["ㅜ"], "1235"],
    "ㅢ": ["2456"],
}

RULE_13_ABBREVIATED_A_DOT = {
    "ㄱ": "1246",
    "ㄴ": RULE_1_CHOSEONG_DOT["ㄴ"],
    "ㄷ": RULE_1_CHOSEONG_DOT["ㄷ"],
    "ㅁ": RULE_1_CHOSEONG_DOT["ㅁ"],
    "ㅂ": RULE_1_CHOSEONG_DOT["ㅂ"],
    "ㅅ": "123",
    "ㅈ": RULE_1_CHOSEONG_DOT["ㅈ"],
    "ㅋ": RULE_1_CHOSEONG_DOT["ㅋ"],
    "ㅌ": RULE_1_CHOSEONG_DOT["ㅌ"],
    "ㅍ": RULE_1_CHOSEONG_DOT["ㅍ"],
    "ㅎ": RULE_1_CHOSEONG_DOT["ㅎ"],
}

RULE_13_TENSE_ABBREVIATED_A_DOTS = {
    "ㄲ": ["6", RULE_13_ABBREVIATED_A_DOT["ㄱ"]],
    "ㄸ": ["6", RULE_13_ABBREVIATED_A_DOT["ㄷ"]],
    "ㅃ": ["6", RULE_13_ABBREVIATED_A_DOT["ㅂ"]],
    "ㅆ": ["6", RULE_13_ABBREVIATED_A_DOT["ㅅ"]],
    "ㅉ": ["6", RULE_13_ABBREVIATED_A_DOT["ㅈ"]],
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


def apply_rule_7_jungseong(jungseong: str) -> Optional[list[str]]:
    return RULE_7_JUNGSEONG_DOTS.get(jungseong)


def apply_rule_13_abbreviated_a_syllable(
    choseong: str,
    jungseong: str,
    jongseong: str,
    next_syllable_starts_with_ieung: bool,
) -> Optional[list[str]]:
    if jungseong != "ㅏ":
        return None

    if next_syllable_starts_with_ieung and choseong in {
        "ㄴ",
        "ㄷ",
        "ㅁ",
        "ㅂ",
        "ㅈ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    }:
        return None

    if choseong in RULE_13_TENSE_ABBREVIATED_A_DOTS:
        return [
            *RULE_13_TENSE_ABBREVIATED_A_DOTS[choseong],
            *encode_jongseong(jongseong),
        ]

    dot = RULE_13_ABBREVIATED_A_DOT.get(choseong)
    if dot is not None:
        return [dot, *encode_jongseong(jongseong)]

    return None


def apply_vowel_jongseong_abbreviation(
    choseong: str,
    jungseong: str,
    jongseong: str,
    next_syllable_starts_with_ieung: bool,
) -> Optional[list[str]]:
    del next_syllable_starts_with_ieung

    abbreviation_dot = {
        ("ㅕ", "ㄹ"): "1256",
        ("ㅕ", "ㅇ"): "12456",
        ("ㅡ", "ㄴ"): "1356",
        ("ㅓ", "ㄴ"): "23456",
        ("ㅕ", "ㄴ"): "16",
        ("ㅗ", "ㅇ"): "123456",
    }.get((jungseong, jongseong))

    if jungseong == "ㅓ" and jongseong == "ㅇ" and choseong == "ㅊ":
        abbreviation_dot = "12456"

    if abbreviation_dot is None:
        return None

    return [*encode_choseong(choseong), abbreviation_dot]


def encode_choseong(choseong: str) -> list[str]:
    if choseong == "ㅇ":
        return []

    tense_dots = apply_rule_2_tense_choseong(choseong)
    if tense_dots is not None:
        return tense_dots

    return [rule_1_choseong_dot(choseong)]


def encode_jungseong(jungseong: str) -> list[str]:
    if jungseong in RULE_6_JUNGSEONG_DOT:
        return [rule_6_jungseong_dot(jungseong)]

    rule_7_dots = apply_rule_7_jungseong(jungseong)
    if rule_7_dots is not None:
        return rule_7_dots

    raise NotImplementedError(f"unsupported jungseong: {jungseong}")


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


SyllableRule = Callable[[str, str, str, bool], Optional[list[str]]]

SYLLABLE_RULES: list[SyllableRule] = [
    apply_rule_13_abbreviated_a_syllable,
    apply_vowel_jongseong_abbreviation,
]


def encode_syllable(
    choseong: str,
    jungseong: str,
    jongseong: str,
    *,
    next_syllable_starts_with_ieung: bool = False,
) -> list[str]:
    for rule in SYLLABLE_RULES:
        result = rule(choseong, jungseong, jongseong, next_syllable_starts_with_ieung)
        if result is not None:
            return result

    return [
        *encode_choseong(choseong),
        *encode_jungseong(jungseong),
        *encode_jongseong(jongseong),
    ]


def encode_standalone_jamo(ch: str, role: str) -> list[str]:
    if role == "standalone":
        if ch in RULE_1_CHOSEONG_DOT or ch in RULE_2_TENSE_CHOSEONG_DOTS:
            return ["123456", *encode_jongseong(ch)]
        return ["123456", *encode_jungseong(ch)]

    if role == "attached_jongseong":
        return ["456", *encode_jongseong(ch)]

    tense_dots = apply_rule_2_tense_choseong(ch)
    if tense_dots is not None:
        return tense_dots

    if role == "jongseong":
        return encode_jongseong(ch)

    if ch in RULE_1_CHOSEONG_DOT:
        return [rule_1_choseong_dot(ch)]

    if ch in RULE_6_JUNGSEONG_DOT:
        return [rule_6_jungseong_dot(ch)]

    rule_7_dots = apply_rule_7_jungseong(ch)
    if rule_7_dots is not None:
        return rule_7_dots

    raise NotImplementedError(f"unsupported standalone jamo: {ch}")
