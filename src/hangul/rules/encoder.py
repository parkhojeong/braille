from .context import RuleContext
from .dispatch import try_encode_rules
from .jamo_encoder import (
    encode_l,
    encode_plain_jamo,
    encode_t,
    encode_v,
)
from .registry import JAMO_ROLE_RULES, SYLLABLE_RULES


def encode_syllable(ctx: RuleContext) -> list[str]:
    result = try_encode_rules(SYLLABLE_RULES, ctx)
    if result is not None:
        return result

    syllable = ctx.syllable
    return [
        *encode_l(syllable.l),
        *encode_v(syllable.v),
        *encode_t(syllable.t),
    ]


def encode_jamo(ch: str, role: str) -> list[str]:
    result = try_encode_rules(JAMO_ROLE_RULES, ch, role)
    if result is not None:
        return result

    return encode_plain_jamo(ch)
