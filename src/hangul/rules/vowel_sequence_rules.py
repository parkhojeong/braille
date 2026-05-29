from collections.abc import Callable

from .dispatch import try_encode_rules
from .tables import VOWEL_SEQUENCE_SEPARATOR_DOT

VowelSequenceRule = Callable[[str, str, str, str, str], list[str] | None]


def rule_11_try_encode_예_구분표(
    v: str,
    t: str,
    next_l: str,
    next_v: str,
    next_t: str,
) -> list[str] | None:
    """제11항 모음자에 ‘예’가 붙어 나올 때에는 그 사이에 구분표 -을 적어 나타낸다."""
    del next_t

    if t == "" and next_l == "ㅇ" and next_v == "ㅖ":
        return [VOWEL_SEQUENCE_SEPARATOR_DOT]
    return None


def rule_12_try_encode_애_구분표(
    v: str,
    t: str,
    next_l: str,
    next_v: str,
    next_t: str,
) -> list[str] | None:
    """제12항 ‘ㅑ, ㅘ, ㅜ, ㅝ’에 ‘애’가 붙어 나올 때에는 두 모음자 사이에 구분표 -을 적어 나타낸다."""
    del next_t

    if (
        t == ""
        and v in {"ㅑ", "ㅘ", "ㅜ", "ㅝ"}
        and next_l == "ㅇ"
        and next_v == "ㅐ"
    ):
        return [VOWEL_SEQUENCE_SEPARATOR_DOT]
    return None


VOWEL_SEQUENCE_RULES: list[VowelSequenceRule] = [
    rule_11_try_encode_예_구분표,
    rule_12_try_encode_애_구분표,
]


def encode_vowel_sequence_separator(
    v: str,
    t: str,
    next_l: str,
    next_v: str,
    next_t: str,
) -> list[str]:
    result = try_encode_rules(
        VOWEL_SEQUENCE_RULES,
        v,
        t,
        next_l,
        next_v,
        next_t,
    )
    if result is not None:
        return result
    return []
