from collections.abc import Callable

from .rules import RuleContext, RuleResult
from .rules.jamo_encoder import encode_t
from .rules.syllable_rules import (
    encode_rule_13_initial,
    should_skip_rule_13_for_following_vowel,
)
from .text import Text

TokenEncoder = Callable[[RuleContext, str], RuleResult]


def encoded_group_length(
    braille_text: Text,
    start: int,
    jamo_role: str,
    encode_token: TokenEncoder,
) -> int:
    group_id = braille_text.tokens[start].group_id
    index = start
    length = 0
    while index < len(braille_text.tokens):
        token = braille_text.tokens[index]
        if token.group_id != group_id:
            break
        encoded = encode_token(braille_text.context_at(index), jamo_role)
        length += len(encoded.dots)
        index += encoded.consumed
    return length


def try_encode_line_break_vowel_exception(
    ctx: RuleContext,
    *,
    line_width: int,
    line_position: int,
) -> RuleResult | None:
    if not ctx.token.is_hangul or not should_skip_rule_13_for_following_vowel(ctx):
        return None

    initial_dots = encode_rule_13_initial(ctx.l)
    if initial_dots is None:
        return None

    abbreviated_dots = [*initial_dots, *encode_t(ctx.t)]
    remaining = line_width - line_position
    if len(abbreviated_dots) > remaining:
        return None

    padding = [""] * (remaining - len(abbreviated_dots))
    return RuleResult([*abbreviated_dots, *padding])


def try_encode_line_aware_token(
    ctx: RuleContext,
    *,
    braille_text: Text,
    jamo_role: str,
    line_width: int,
    line_position: int,
    encode_token: TokenEncoder,
) -> RuleResult | None:
    group_length = encoded_group_length(
        braille_text,
        ctx.index,
        jamo_role,
        encode_token,
    )
    if line_position + group_length <= line_width:
        return None

    return try_encode_line_break_vowel_exception(
        ctx,
        line_width=line_width,
        line_position=line_position,
    )
