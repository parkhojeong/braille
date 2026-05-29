from collections.abc import Callable

from .jamo_basic_rules import (
    rule_1_try_encode_l_ㅇ,
    rule_2_try_encode_l_ㄲㄸㅃㅆㅉ,
    rule_4_try_encode_t_ㄲㅆ,
    rule_5_try_encode_t_cluster,
    rule_7_try_encode_v_cluster,
)

JamoPartRule = Callable[[str], list[str] | None]

L_RULES: list[JamoPartRule] = [
    rule_1_try_encode_l_ㅇ,
    rule_2_try_encode_l_ㄲㄸㅃㅆㅉ,
]

V_RULES: list[JamoPartRule] = [
    rule_7_try_encode_v_cluster,
]

T_RULES: list[JamoPartRule] = [
    rule_4_try_encode_t_ㄲㅆ,
    rule_5_try_encode_t_cluster,
]
