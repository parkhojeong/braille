from .context import RuleContext
from .jamo_encoder import encode_l, encode_t, encode_v
from .jamo_basic_rules import encode_tense_l
from .rule_tables import (
    RULE_13_A_ABBREVIATION_DOTS,
    RULE_13_VOWEL_FOLLOWING_EXCEPTION_L,
    RULE_15_LVT_ABBREVIATION_DOTS,
    RULE_15_T_CLUSTER_PARTS,
    RULE_15_VT_ABBREVIATION_DOTS,
    RULE_17_ABBREVIATION_DOTS,
)


def rule_14_try_encode_팠(
    ctx: RuleContext,
) -> list[str] | None:
    """[붙임] ‘팠’을 적을 때에는 ‘ㅏ’를 생략하지 않고 적는다."""
    if ctx.l == "ㅍ" and ctx.v == "ㅏ" and ctx.t == "ㅆ":
        return [*encode_l(ctx.l), *encode_v(ctx.v), *encode_t(ctx.t)]
    return None


def should_skip_rule_13_for_following_vowel(ctx: RuleContext) -> bool:
    return (
        ctx.t == ""
        and ctx.next_syllable is not None
        and ctx.next_syllable[0] == "ㅇ"
        and ctx.l in RULE_13_VOWEL_FOLLOWING_EXCEPTION_L
    )


def encode_rule_13_initial(l: str) -> list[str] | None:
    tense_dots = encode_tense_l(l, RULE_13_A_ABBREVIATION_DOTS)
    if tense_dots is not None:
        return tense_dots

    dot = RULE_13_A_ABBREVIATION_DOTS.get(l)
    if dot is not None:
        return [dot]

    return None


def rule_13_try_encode_ㅏ_약자(
    ctx: RuleContext,
) -> list[str] | None:
    """제13항 다음 글자들은 약자를 사용하여 적는다.

    [붙임] 위의 글자들에 받침이 있거나 첫소리가 된소리일 때에도 약자를 사용하여 적는다.
    제14항 ‘나, 다, 마, 바, 자, 카, 타, 파, 하’에 모음이 붙어 나올 때에는 약자를 사용하지 않는다.
    """
    if ctx.v != "ㅏ" or should_skip_rule_13_for_following_vowel(ctx):
        return None

    initial_dots = encode_rule_13_initial(ctx.l)
    if initial_dots is None:
        return None

    return [*initial_dots, *encode_t(ctx.t)]


def rule_15_vt_dots() -> dict[tuple[str, str], str]:
    return dict(RULE_15_VT_ABBREVIATION_DOTS)


def rule_15_split_t(t: str) -> list[str] | None:
    parts = RULE_15_T_CLUSTER_PARTS.get(t)
    if parts is not None:
        return [*parts]
    return None


def rule_15_try_encode_기본_약자(
    ctx: RuleContext,
) -> list[str] | None:
    """제15항 다음 글자들은 약자를 사용하여 적는다."""
    syllable_dots = RULE_15_LVT_ABBREVIATION_DOTS.get((ctx.l, ctx.v, ctx.t))
    if syllable_dots is not None:
        return [*syllable_dots]

    if (ctx.l, ctx.v, ctx.t) == ("ㅅ", "ㅕ", "ㅇ"):
        return None

    abbreviation_dot = RULE_15_VT_ABBREVIATION_DOTS.get((ctx.v, ctx.t))
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

    abbreviation_dot = RULE_15_VT_ABBREVIATION_DOTS.get((ctx.v, parts[0]))
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

    abbreviation_dot = RULE_17_ABBREVIATION_DOTS.get((ctx.l, ctx.v, ctx.t))
    if abbreviation_dot is None:
        return None

    return [*encode_l(ctx.l), abbreviation_dot]
