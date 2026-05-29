from .context import RuleContext, RuleResult
from .punctuation_tables import TEXT_PUNCTUATION_DOTS


def encode_punctuation(ctx: RuleContext) -> RuleResult | None:
    if ctx.token.kind != "PUNCTUATION":
        return None

    dots = TEXT_PUNCTUATION_DOTS.get(ctx.token.text)
    if dots is None:
        return None
    return RuleResult(dots)
