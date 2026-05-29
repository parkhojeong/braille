from collections.abc import Callable

from .context import RuleContext, RuleResult
from .punctuation_tables import TEXT_PUNCTUATION_DOTS

PunctuationRule = Callable[[RuleContext], RuleResult | None]


def rule_text_punctuation(ctx: RuleContext) -> RuleResult | None:
    if not ctx.token.is_punctuation:
        return None

    dots = TEXT_PUNCTUATION_DOTS.get(ctx.token.text)
    if dots is None:
        return None
    return RuleResult(dots)


PUNCTUATION_RULES: list[PunctuationRule] = [
    rule_text_punctuation,
]


def encode_punctuation(ctx: RuleContext) -> RuleResult | None:
    for rule in PUNCTUATION_RULES:
        result = rule(ctx)
        if result is not None:
            return result
    return None
