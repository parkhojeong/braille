from collections.abc import Callable

from .context import RuleContext, RuleResult
from .punctuation_tables import TEXT_PUNCTUATION_DOTS

PunctuationRule = Callable[[RuleContext], RuleResult | None]


def next_non_space_token(ctx: RuleContext):
    index = ctx.index + 1
    while index < len(ctx.tokens) and ctx.tokens[index].is_space:
        index += 1
    if index >= len(ctx.tokens):
        return None
    return ctx.tokens[index]


def rule_latin_sequence_comma(ctx: RuleContext) -> RuleResult | None:
    if not ctx.token.is_punctuation or ctx.token.text != ",":
        return None
    if ctx.previous_token is None or not ctx.previous_token.is_latin:
        return None

    next_token = next_non_space_token(ctx)
    if next_token is None or not (next_token.is_latin or next_token.is_number):
        return None
    return RuleResult(["2"])


def rule_text_punctuation(ctx: RuleContext) -> RuleResult | None:
    if not ctx.token.is_punctuation:
        return None

    dots = TEXT_PUNCTUATION_DOTS.get(ctx.token.text)
    if dots is None:
        return None
    return RuleResult(dots)


PUNCTUATION_RULES: list[PunctuationRule] = [
    rule_latin_sequence_comma,
    rule_text_punctuation,
]


def encode_punctuation(ctx: RuleContext) -> RuleResult | None:
    for rule in PUNCTUATION_RULES:
        result = rule(ctx)
        if result is not None:
            return result
    return None
