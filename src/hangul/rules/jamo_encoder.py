from .dispatch import try_encode_rules
from .jamo_basic_rules import (
    rule_1_encode_l,
    rule_2_try_encode_l_ㄲㄸㅃㅆㅉ,
    rule_3_encode_t,
    rule_6_encode_v,
)
from .jamo_registry import L_RULES, T_RULES, V_RULES
from .tables import L_DOTS, V_DOTS


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


def encode_plain_jamo(ch: str) -> list[str]:
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
