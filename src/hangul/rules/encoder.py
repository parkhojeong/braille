from collections.abc import Callable

from .context import RuleContext
from .dispatch import try_encode_rules
from .jamo import (
    encode_l,
    encode_t,
    encode_v,
    rule_1_encode_l,
    rule_2_try_encode_l_ㄲㄸㅃㅆㅉ,
    rule_3_to_5_try_encode_t_role,
    rule_6_encode_v,
    rule_7_try_encode_v_cluster,
    rule_8_or_9_try_encode_standalone_jamo,
    rule_10_try_encode_attached_t,
)
from .syllable import (
    rule_13_try_encode_ㅏ_약자,
    rule_14_try_encode_팠,
    rule_15_try_encode_기본_약자,
    rule_15_try_encode_포함_약자,
    rule_16_try_encode_껏,
    rule_17_try_encode_성썽정쩡청,
)
from .tables import L_DOTS, V_DOTS

JamoRoleRule = Callable[[str, str], list[str] | None]
SyllableRule = Callable[[RuleContext], list[str] | None]

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

    result = rule_7_try_encode_v_cluster(ch)
    if result is not None:
        return result

    raise NotImplementedError(f"unsupported jamo: {ch}")
