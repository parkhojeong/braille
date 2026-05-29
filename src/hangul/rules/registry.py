from collections.abc import Callable

from .context import RuleContext
from .jamo import (
    rule_3_to_5_try_encode_t_role,
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

JamoRoleRule = Callable[[str, str], list[str] | None]
SyllableRule = Callable[[RuleContext], list[str] | None]

# Rule order is part of the encoding behavior: earlier rules win.
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
