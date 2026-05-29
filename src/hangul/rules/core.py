from collections.abc import Callable, Sequence

from .tables import (
    ABBREVIATED_A_DOTS,
    ATTACHED_CONSONANT_SIGN_DOT,
    L_DOTS,
    T_CLUSTER_DOTS,
    V_CLUSTER_DOTS,
    RULE_4_T_ㄲㅆ_DOTS,
    FULL_SIGN_DOT,
    T_DOTS,
    V_DOTS,
    NEXT_L_ㅇ_CANCELS_ABBREVIATED_A,
    RULE_12_PRECEDING_V,
    RULE_15_SYLLABLE_ABBREVIATIONS,
    RULE_15_V_T_ABBREVIATIONS,
    RULE_17_LVT_ABBREVIATIONS,
    TENSE_ABBREVIATED_A_DOTS,
    RULE_2_L_ㄲㄸㅃㅆㅉ_DOTS,
    VOWEL_SEQUENCE_SEPARATOR_DOT,
)


def encode_dot(mapping: dict[str, str], key: str, label: str) -> list[str]:
    try:
        return [mapping[key]]
    except KeyError:
        raise NotImplementedError(f"unsupported {label}: {key}") from None


Rule = Callable[..., list[str] | None]


def try_encode_rules(rules: Sequence[Rule], *args: object) -> list[str] | None:
    for rule in rules:
        result = rule(*args)
        if result is not None:
            return result
    return None


def rule_1_encode_l(l: str) -> list[str]:
    return encode_dot(L_DOTS, l, "l")


def rule_1_try_encode_l_ㅇ(l: str) -> list[str] | None:
    if l == "ㅇ":
        return []
    return None


def rule_2_try_encode_l_ㄲㄸㅃㅆㅉ(l: str) -> list[str] | None:
    return RULE_2_L_ㄲㄸㅃㅆㅉ_DOTS.get(l)


def rule_3_encode_t(t: str) -> list[str]:
    return encode_dot(T_DOTS, t, "t")


def rule_4_try_encode_t_ㄲㅆ(t: str) -> list[str] | None:
    return RULE_4_T_ㄲㅆ_DOTS.get(t)


def rule_5_try_encode_t_cluster(t: str) -> list[str] | None:
    return T_CLUSTER_DOTS.get(t)


def rule_6_encode_v(v: str) -> list[str]:
    return encode_dot(V_DOTS, v, "v")


def rule_7_try_encode_v_cluster(v: str) -> list[str] | None:
    return V_CLUSTER_DOTS.get(v)


def rule_3_to_5_try_encode_t_role(ch: str, role: str) -> list[str] | None:
    if role == "t":
        return encode_t(ch)
    return None


def rule_8_or_9_try_encode_standalone_jamo(ch: str, role: str) -> list[str] | None:
    if role != "standalone":
        return None

    if ch in L_DOTS or ch in RULE_2_L_ㄲㄸㅃㅆㅉ_DOTS:
        return [FULL_SIGN_DOT, *encode_t(ch)]
    return [FULL_SIGN_DOT, *encode_v(ch)]


def rule_10_try_encode_attached_consonant(ch: str, role: str) -> list[str] | None:
    if role != "attached_t":
        return None

    return [ATTACHED_CONSONANT_SIGN_DOT, *encode_t(ch)]


def rule_11_try_encode_예_구분표(
    v: str,
    t: str,
    next_l: str,
    next_v: str,
    next_t: str,
) -> list[str] | None:
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
    del next_t

    if (
        t == ""
        and v in RULE_12_PRECEDING_V
        and next_l == "ㅇ"
        and next_v == "ㅐ"
    ):
        return [VOWEL_SEQUENCE_SEPARATOR_DOT]
    return None


def rule_14_try_encode_팠(
    l: str,
    v: str,
    t: str,
    next_syllable_l_is_ㅇ: bool,
) -> list[str] | None:
    del next_syllable_l_is_ㅇ

    if l == "ㅍ" and v == "ㅏ" and t == "ㅆ":
        return [*encode_l(l), *encode_v(v), *encode_t(t)]
    return None


def rule_13_try_encode_abbreviated_a_syllable(
    l: str,
    v: str,
    t: str,
    next_syllable_l_is_ㅇ: bool,
) -> list[str] | None:
    if v != "ㅏ":
        return None

    if (
        next_syllable_l_is_ㅇ
        and l in NEXT_L_ㅇ_CANCELS_ABBREVIATED_A
    ):
        return None

    tense_dots = TENSE_ABBREVIATED_A_DOTS.get(l)
    if tense_dots is not None:
        return [*tense_dots, *encode_t(t)]

    dot = ABBREVIATED_A_DOTS.get(l)
    if dot is not None:
        return [dot, *encode_t(t)]

    return None


def rule_15_try_encode_abbreviated_syllable(
    l: str,
    v: str,
    t: str,
    next_syllable_l_is_ㅇ: bool,
) -> list[str] | None:
    del next_syllable_l_is_ㅇ

    syllable_dots = RULE_15_SYLLABLE_ABBREVIATIONS.get(
        (l, v, t)
    )
    if syllable_dots is not None:
        return syllable_dots

    abbreviation_dot = RULE_15_V_T_ABBREVIATIONS.get(
        (v, t)
    )

    if abbreviation_dot is None:
        return None

    return [*encode_l(l), abbreviation_dot]


def rule_17_try_encode_성썽정쩡청(
    l: str,
    v: str,
    t: str,
    next_syllable_l_is_ㅇ: bool,
) -> list[str] | None:
    del next_syllable_l_is_ㅇ

    abbreviation_dot = RULE_17_LVT_ABBREVIATIONS.get(
        (l, v, t)
    )
    if abbreviation_dot is None:
        return None

    return [*encode_l(l), abbreviation_dot]


def encode_l(l: str) -> list[str]:
    result = try_encode_rules(L_RULES, l)
    if result is not None:
        return result

    return rule_1_encode_l(l)


def encode_v(v: str) -> list[str]:
    if v in V_DOTS:
        return rule_6_encode_v(v)

    result = try_encode_rules(V_RULES, v)
    if result is not None:
        return result

    raise NotImplementedError(f"unsupported v: {v}")


def encode_t(t: str) -> list[str]:
    if not t:
        return []

    result = try_encode_rules(T_RULES, t)
    if result is not None:
        return result

    return rule_3_encode_t(t)


SyllableRule = Callable[[str, str, str, bool], list[str] | None]
JamoRoleRule = Callable[[str, str], list[str] | None]
VowelSequenceRule = Callable[[str, str, str, str, str], list[str] | None]

L_RULES: list[Callable[[str], list[str] | None]] = [
    rule_1_try_encode_l_ㅇ,
    rule_2_try_encode_l_ㄲㄸㅃㅆㅉ,
]

V_RULES: list[Callable[[str], list[str] | None]] = [
    rule_7_try_encode_v_cluster,
]

T_RULES: list[Callable[[str], list[str] | None]] = [
    rule_4_try_encode_t_ㄲㅆ,
    rule_5_try_encode_t_cluster,
]

VOWEL_SEQUENCE_RULES: list[VowelSequenceRule] = [
    rule_11_try_encode_예_구분표,
    rule_12_try_encode_애_구분표,
]

SYLLABLE_RULES: list[SyllableRule] = [
    rule_14_try_encode_팠,
    rule_13_try_encode_abbreviated_a_syllable,
    rule_15_try_encode_abbreviated_syllable,
    rule_17_try_encode_성썽정쩡청,
]

JAMO_ROLE_RULES: list[JamoRoleRule] = [
    rule_8_or_9_try_encode_standalone_jamo,
    rule_10_try_encode_attached_consonant,
    rule_3_to_5_try_encode_t_role,
]


def encode_syllable(
    l: str,
    v: str,
    t: str,
    *,
    next_syllable_l_is_ㅇ: bool = False,
) -> list[str]:
    result = try_encode_rules(
        SYLLABLE_RULES,
        l,
        v,
        t,
        next_syllable_l_is_ㅇ,
    )
    if result is not None:
        return result

    return [
        *encode_l(l),
        *encode_v(v),
        *encode_t(t),
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


def encode_jamo(ch: str, role: str) -> list[str]:
    result = try_encode_rules(JAMO_ROLE_RULES, ch, role)
    if result is not None:
        return result

    result = rule_2_try_encode_l_ㄲㄸㅃㅆㅉ(ch)
    if result is not None:
        return result

    if ch in L_DOTS:
        return rule_1_encode_l(ch)

    if ch in V_DOTS:
        return rule_6_encode_v(ch)

    result = try_encode_rules(V_RULES, ch)
    if result is not None:
        return result

    raise NotImplementedError(f"unsupported jamo: {ch}")
