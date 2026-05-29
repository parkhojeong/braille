from braille.ascii import ascii_to_dots

from .context import RuleContext, RuleResult
from .symbol_tables import TEXT_SYMBOL_ASCII


def encode_symbol(ctx: RuleContext) -> RuleResult | None:
    if not ctx.token.is_symbol:
        return None

    ascii_text = TEXT_SYMBOL_ASCII.get(ctx.token.text)
    if ascii_text is None:
        return None
    return RuleResult(ascii_to_dots(ascii_text))
