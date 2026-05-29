from collections.abc import Callable, Sequence

from .context import RuleContext
from .tables import (
    FULL_SIGN_DOT,
    L_DOTS,
    RULE_10_ATTACHED_T_SIGN_DOT,
    T_DOTS,
    V_DOTS,
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
    """제1항 기본 자음자 14개가 첫소리로 쓰일 때에는 다음과 같이 적는다."""
    return encode_dot(L_DOTS, l, "l")


def rule_1_try_encode_l_ㅇ(l: str) -> list[str] | None:
    """[다만1] ‘ㅇ’이 첫소리로 쓰일 때에는 점자로 이를 표기하지 않는다."""
    if l == "ㅇ":
        return []
    return None


def rule_2_try_encode_l_ㄲㄸㅃㅆㅉ(l: str) -> list[str] | None:
    """제2항 된소리 글자 ‘ㄲ, ㄸ, ㅃ, ㅆ, ㅉ’이 첫소리로 쓰일 때에는 ‘ㄱ, ㄷ, ㅂ, ㅅ, ㅈ’ 앞에 된소리표 ,을 적어 나타낸다."""
    dots = {
        "ㄲ": ["6", L_DOTS["ㄱ"]],
        "ㄸ": ["6", L_DOTS["ㄷ"]],
        "ㅃ": ["6", L_DOTS["ㅂ"]],
        "ㅆ": ["6", L_DOTS["ㅅ"]],
        "ㅉ": ["6", L_DOTS["ㅈ"]],
    }
    return dots.get(l)


def rule_3_encode_t(t: str) -> list[str]:
    """제3항 기본 자음자 14개가 받침으로 쓰일 때에는 다음과 같이 적는다."""
    return encode_dot(T_DOTS, t, "t")


def rule_4_try_encode_t_ㄲㅆ(t: str) -> list[str] | None:
    """제4항 쌍받침 ‘ㄲ’은 aa으로 적고, 쌍받침 ‘ㅆ’은 약자인 /으로 적는다."""
    dots = {
        "ㄲ": [T_DOTS["ㄱ"], T_DOTS["ㄱ"]],
        "ㅆ": [T_DOTS["ㅆ"]],
    }
    return dots.get(t)


def rule_5_try_encode_t_cluster(t: str) -> list[str] | None:
    """제5항 겹받침은 각 받침 글자를 어울러 다음과 같이 적는다."""
    dots = {
        "ㄳ": [T_DOTS["ㄱ"], T_DOTS["ㅅ"]],
        "ㄵ": [T_DOTS["ㄴ"], T_DOTS["ㅈ"]],
        "ㄶ": [T_DOTS["ㄴ"], T_DOTS["ㅎ"]],
        "ㄺ": [T_DOTS["ㄹ"], T_DOTS["ㄱ"]],
        "ㄻ": [T_DOTS["ㄹ"], T_DOTS["ㅁ"]],
        "ㄼ": [T_DOTS["ㄹ"], T_DOTS["ㅂ"]],
        "ㄽ": [T_DOTS["ㄹ"], T_DOTS["ㅅ"]],
        "ㄾ": [T_DOTS["ㄹ"], T_DOTS["ㅌ"]],
        "ㄿ": [T_DOTS["ㄹ"], T_DOTS["ㅍ"]],
        "ㅀ": [T_DOTS["ㄹ"], T_DOTS["ㅎ"]],
        "ㅄ": [T_DOTS["ㅂ"], T_DOTS["ㅅ"]],
    }
    return dots.get(t)


def rule_6_encode_v(v: str) -> list[str]:
    """제6항 기본 모음자 10개는 다음과 같이 적는다."""
    return encode_dot(V_DOTS, v, "v")


def rule_7_try_encode_v_cluster(v: str) -> list[str] | None:
    """제7항 그 밖의 모음자 11개는 다음과 같이 적는다."""
    dots = {
        "ㅐ": ["1235"],
        "ㅒ": [V_DOTS["ㅑ"], "1235"],
        "ㅔ": ["1345"],
        "ㅖ": ["34"],
        "ㅘ": ["1236"],
        "ㅙ": ["1236", "1235"],
        "ㅚ": ["13456"],
        "ㅝ": ["1234"],
        "ㅞ": ["1234", "1235"],
        "ㅟ": [V_DOTS["ㅜ"], "1235"],
        "ㅢ": ["2456"],
    }
    return dots.get(v)


def rule_3_to_5_try_encode_t_role(ch: str, role: str) -> list[str] | None:
    """자모가 받침 역할이면 제3~5항의 받침 규칙으로 적는다."""
    if role == "t":
        return encode_t(ch)
    return None


def rule_8_or_9_try_encode_standalone_jamo(ch: str, role: str) -> list[str] | None:
    """제8항 자음자나 모음자가 단독으로 쓰일 때에는 해당 글자 앞에 온표 =을 적어 나타내며, 자음자는 받침으로 적는다.

    제9항 한글의 자음자가 번호로 쓰일 때에는 온표를 앞세워 받침으로 적는다.
    """
    if role != "standalone":
        return None

    if ch in L_DOTS or rule_2_try_encode_l_ㄲㄸㅃㅆㅉ(ch) is not None:
        return [FULL_SIGN_DOT, *encode_t(ch)]
    return [FULL_SIGN_DOT, *encode_v(ch)]


def rule_10_try_encode_attached_t(ch: str, role: str) -> list[str] | None:
    """제10항 단독으로 쓰인 자음자가 단어에 붙어 나올 때에는 _을 앞세워 받침으로 적는다."""
    if role != "attached_t":
        return None

    return [RULE_10_ATTACHED_T_SIGN_DOT, *encode_t(ch)]


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


def rule_14_try_encode_팠(
    ctx: RuleContext,
) -> list[str] | None:
    """[붙임] ‘팠’을 적을 때에는 ‘ㅏ’를 생략하지 않고 적는다."""
    if ctx.l == "ㅍ" and ctx.v == "ㅏ" and ctx.t == "ㅆ":
        return [*encode_l(ctx.l), *encode_v(ctx.v), *encode_t(ctx.t)]
    return None


def rule_13_try_encode_ㅏ_약자(
    ctx: RuleContext,
) -> list[str] | None:
    """제13항 다음 글자들은 약자를 사용하여 적는다.

    [붙임] 위의 글자들에 받침이 있거나 첫소리가 된소리일 때에도 약자를 사용하여 적는다.
    제14항 ‘나, 다, 마, 바, 자, 카, 타, 파, 하’에 모음이 붙어 나올 때에는 약자를 사용하지 않는다.
    """
    if ctx.v != "ㅏ":
        return None

    if (
        ctx.t == ""
        and ctx.next_syllable is not None
        and ctx.next_syllable[0] == "ㅇ"
        and ctx.l in {"ㄴ", "ㄷ", "ㅁ", "ㅂ", "ㅈ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"}
    ):
        return None

    dots = {
        "ㄱ": "1246",
        "ㄴ": L_DOTS["ㄴ"],
        "ㄷ": L_DOTS["ㄷ"],
        "ㅁ": L_DOTS["ㅁ"],
        "ㅂ": L_DOTS["ㅂ"],
        "ㅅ": "123",
        "ㅈ": L_DOTS["ㅈ"],
        "ㅋ": L_DOTS["ㅋ"],
        "ㅌ": L_DOTS["ㅌ"],
        "ㅍ": L_DOTS["ㅍ"],
        "ㅎ": L_DOTS["ㅎ"],
    }
    ㄲㄸㅃㅆㅉ_dots = {
        "ㄲ": ["6", dots["ㄱ"]],
        "ㄸ": ["6", dots["ㄷ"]],
        "ㅃ": ["6", dots["ㅂ"]],
        "ㅆ": ["6", dots["ㅅ"]],
        "ㅉ": ["6", dots["ㅈ"]],
    }

    tense_dots = ㄲㄸㅃㅆㅉ_dots.get(ctx.l)
    if tense_dots is not None:
        return [*tense_dots, *encode_t(ctx.t)]

    dot = dots.get(ctx.l)
    if dot is not None:
        return [dot, *encode_t(ctx.t)]

    return None


def rule_15_vt_dots() -> dict[tuple[str, str], str]:
    return {
        ("ㅓ", "ㄱ"): "1456",
        ("ㅓ", "ㄴ"): "23456",
        ("ㅓ", "ㄹ"): "2345",
        ("ㅕ", "ㄴ"): "16",
        ("ㅕ", "ㄹ"): "1256",
        ("ㅕ", "ㅇ"): "12456",
        ("ㅗ", "ㄱ"): "1346",
        ("ㅗ", "ㄴ"): "12356",
        ("ㅗ", "ㅇ"): "123456",
        ("ㅜ", "ㄴ"): "1245",
        ("ㅜ", "ㄹ"): "12346",
        ("ㅡ", "ㄴ"): "1356",
        ("ㅡ", "ㄹ"): "2346",
        ("ㅣ", "ㄴ"): "12345",
    }


def rule_15_split_t(t: str) -> list[str] | None:
    parts = {
        "ㄲ": ["ㄱ", "ㄱ"],
        "ㄳ": ["ㄱ", "ㅅ"],
        "ㄵ": ["ㄴ", "ㅈ"],
        "ㄶ": ["ㄴ", "ㅎ"],
        "ㄺ": ["ㄹ", "ㄱ"],
        "ㄻ": ["ㄹ", "ㅁ"],
        "ㄼ": ["ㄹ", "ㅂ"],
        "ㄽ": ["ㄹ", "ㅅ"],
        "ㄾ": ["ㄹ", "ㅌ"],
        "ㄿ": ["ㄹ", "ㅍ"],
        "ㅀ": ["ㄹ", "ㅎ"],
    }
    return parts.get(t)


def rule_15_try_encode_기본_약자(
    ctx: RuleContext,
) -> list[str] | None:
    """제15항 다음 글자들은 약자를 사용하여 적는다."""
    lvt_dots = {
        ("ㄱ", "ㅓ", "ㅅ"): ["456", "234"],
    }
    syllable_dots = lvt_dots.get((ctx.l, ctx.v, ctx.t))
    if syllable_dots is not None:
        return syllable_dots

    if (ctx.l, ctx.v, ctx.t) == ("ㅅ", "ㅕ", "ㅇ"):
        return None

    abbreviation_dot = rule_15_vt_dots().get((ctx.v, ctx.t))

    if abbreviation_dot is not None:
        return [*encode_l(ctx.l), abbreviation_dot]

    return None


def rule_15_try_encode_포함_약자(
    ctx: RuleContext,
) -> list[str] | None:
    """[붙임] ‘억, 언, 얼, 연, 열, 영, 옥, 온, 옹, 운, 울, 은, 을, 인, 것’이 포함되어 있는 글자에도 약자를 사용하여 적는다."""
    parts = rule_15_split_t(ctx.t)
    if parts is None:
        return None

    abbreviation_dot = rule_15_vt_dots().get((ctx.v, parts[0]))
    if abbreviation_dot is None:
        return None

    remaining_t_dots = [
        dot
        for remaining_t in parts[1:]
        for dot in encode_t(remaining_t)
    ]
    return [*encode_l(ctx.l), abbreviation_dot, *remaining_t_dots]


def rule_16_try_encode_껏(
    ctx: RuleContext,
) -> list[str] | None:
    """제16항 ‘까, 싸, 껏’을 적을 때에는 ‘가, 사, 것’의 약자 앞에 된소리표를 적어 나타낸다."""
    if ctx.l == "ㄲ" and ctx.v == "ㅓ" and ctx.t == "ㅅ":
        return ["6", *rule_15_encode_것()]
    return None


def rule_15_encode_것() -> list[str]:
    return ["456", "234"]


def rule_17_try_encode_성썽정쩡청(
    ctx: RuleContext,
) -> list[str] | None:
    """제17항 ‘성, 썽, 정, 쩡, 청’을 적을 때에는 ‘ㅅ, ㅆ, ㅈ, ㅉ, ㅊ’ 다음에 ‘영’의 약자 }을 적어 나타낸다."""
    if (ctx.l, ctx.v, ctx.t) == ("ㅈ", "ㅓ", "ㅇ") and ctx.next_syllable == (
        "ㅅ",
        "ㅓ",
        "ㅇ",
    ):
        return encode_l(ctx.l)

    dots = {
        ("ㅅ", "ㅓ", "ㅇ"): "12456",
        ("ㅆ", "ㅓ", "ㅇ"): "12456",
        ("ㅈ", "ㅓ", "ㅇ"): "12456",
        ("ㅉ", "ㅓ", "ㅇ"): "12456",
        ("ㅊ", "ㅓ", "ㅇ"): "12456",
    }
    abbreviation_dot = dots.get((ctx.l, ctx.v, ctx.t))
    if abbreviation_dot is None:
        return None

    return [*encode_l(ctx.l), abbreviation_dot]


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


SyllableRule = Callable[[RuleContext], list[str] | None]
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
    rule_13_try_encode_ㅏ_약자,
    rule_16_try_encode_껏,
    rule_15_try_encode_기본_약자,
    rule_15_try_encode_포함_약자,
    rule_17_try_encode_성썽정쩡청,
]

JAMO_ROLE_RULES: list[JamoRoleRule] = [
    rule_8_or_9_try_encode_standalone_jamo,
    rule_10_try_encode_attached_t,
    rule_3_to_5_try_encode_t_role,
]


def encode_syllable(ctx: RuleContext) -> list[str]:
    result = try_encode_rules(SYLLABLE_RULES, ctx)
    if result is not None:
        return result

    return [
        *encode_l(ctx.l),
        *encode_v(ctx.v),
        *encode_t(ctx.t),
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
