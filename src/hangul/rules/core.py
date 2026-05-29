from collections.abc import Callable

from .tables import (
    ABBREVIATED_A_DOTS,
    ATTACHED_CONSONANT_SIGN_DOT,
    CHOSEONG_DOTS,
    COMPOSITE_JONGSEONG_DOTS,
    COMPOSITE_JUNGSEONG_DOTS,
    DOUBLE_JONGSEONG_DOTS,
    FULL_SIGN_DOT,
    JONGSEONG_DOTS,
    JUNGSEONG_DOTS,
    NEXT_IEUNG_CANCELS_ABBREVIATED_A,
    RULE_15_SYLLABLE_ABBREVIATIONS,
    RULE_15_VOWEL_JONGSEONG_ABBREVIATIONS,
    RULE_17_YEONG_AFTER_CONSONANT_ABBREVIATIONS,
    TENSE_ABBREVIATED_A_DOTS,
    TENSE_CHOSEONG_DOTS,
)


def lookup(mapping: dict[str, str], key: str, label: str) -> str:
    try:
        return mapping[key]
    except KeyError:
        raise NotImplementedError(f"unsupported {label}: {key}") from None


def rule_1_choseong_dot(choseong: str) -> str:
    return lookup(CHOSEONG_DOTS, choseong, "choseong")


def apply_rule_2_tense_choseong(choseong: str) -> list[str] | None:
    return TENSE_CHOSEONG_DOTS.get(choseong)


def rule_3_jongseong_dot(jongseong: str) -> str:
    return lookup(JONGSEONG_DOTS, jongseong, "jongseong")


def apply_rule_4_double_jongseong(jongseong: str) -> list[str] | None:
    return DOUBLE_JONGSEONG_DOTS.get(jongseong)


def apply_rule_5_composite_jongseong(jongseong: str) -> list[str] | None:
    return COMPOSITE_JONGSEONG_DOTS.get(jongseong)


def rule_6_jungseong_dot(jungseong: str) -> str:
    return lookup(JUNGSEONG_DOTS, jungseong, "jungseong")


def apply_rule_7_jungseong(jungseong: str) -> list[str] | None:
    return COMPOSITE_JUNGSEONG_DOTS.get(jungseong)


def apply_rule_13_abbreviated_a_syllable(
    choseong: str,
    jungseong: str,
    jongseong: str,
    next_syllable_starts_with_ieung: bool,
) -> list[str] | None:
    if jungseong != "ㅏ":
        return None

    if (
        next_syllable_starts_with_ieung
        and choseong in NEXT_IEUNG_CANCELS_ABBREVIATED_A
    ):
        return None

    tense_dots = TENSE_ABBREVIATED_A_DOTS.get(choseong)
    if tense_dots is not None:
        return [*tense_dots, *encode_jongseong(jongseong)]

    dot = ABBREVIATED_A_DOTS.get(choseong)
    if dot is not None:
        return [dot, *encode_jongseong(jongseong)]

    return None


def apply_rule_15_vowel_jongseong_abbreviation(
    choseong: str,
    jungseong: str,
    jongseong: str,
    next_syllable_starts_with_ieung: bool,
) -> list[str] | None:
    del next_syllable_starts_with_ieung

    syllable_dots = RULE_15_SYLLABLE_ABBREVIATIONS.get(
        (choseong, jungseong, jongseong)
    )
    if syllable_dots is not None:
        return syllable_dots

    abbreviation_dot = RULE_15_VOWEL_JONGSEONG_ABBREVIATIONS.get(
        (jungseong, jongseong)
    )

    if abbreviation_dot is None:
        return None

    return [*encode_choseong(choseong), abbreviation_dot]


def apply_rule_17_yeong_after_consonant_abbreviation(
    choseong: str,
    jungseong: str,
    jongseong: str,
    next_syllable_starts_with_ieung: bool,
) -> list[str] | None:
    del next_syllable_starts_with_ieung

    abbreviation_dot = RULE_17_YEONG_AFTER_CONSONANT_ABBREVIATIONS.get(
        (choseong, jungseong, jongseong)
    )
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
    if jungseong in JUNGSEONG_DOTS:
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


SyllableRule = Callable[[str, str, str, bool], list[str] | None]

SYLLABLE_RULES: list[SyllableRule] = [
    apply_rule_13_abbreviated_a_syllable,
    apply_rule_15_vowel_jongseong_abbreviation,
    apply_rule_17_yeong_after_consonant_abbreviation,
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
        return apply_rule_8_or_9_standalone_jamo(ch)

    if role == "attached_jongseong":
        return apply_rule_10_attached_consonant(ch)

    tense_dots = apply_rule_2_tense_choseong(ch)
    if tense_dots is not None:
        return tense_dots

    if role == "jongseong":
        return encode_jongseong(ch)

    if ch in CHOSEONG_DOTS:
        return [rule_1_choseong_dot(ch)]

    if ch in JUNGSEONG_DOTS:
        return [rule_6_jungseong_dot(ch)]

    rule_7_dots = apply_rule_7_jungseong(ch)
    if rule_7_dots is not None:
        return rule_7_dots

    raise NotImplementedError(f"unsupported standalone jamo: {ch}")


def apply_rule_8_or_9_standalone_jamo(ch: str) -> list[str]:
    if ch in CHOSEONG_DOTS or ch in TENSE_CHOSEONG_DOTS:
        return [FULL_SIGN_DOT, *encode_jongseong(ch)]
    return [FULL_SIGN_DOT, *encode_jungseong(ch)]


def apply_rule_10_attached_consonant(ch: str) -> list[str]:
    return [ATTACHED_CONSONANT_SIGN_DOT, *encode_jongseong(ch)]
