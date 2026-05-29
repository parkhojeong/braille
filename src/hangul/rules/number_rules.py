from braille.ascii import ascii_to_dots

from .context import RuleContext, RuleResult
from .number_tables import NUMBER_ASCII


def encode_number_ascii(text: str) -> str:
    return f"#{''.join(NUMBER_ASCII[digit] for digit in text)}"


def encode_number(ctx: RuleContext) -> RuleResult | None:
    if not ctx.token.is_number:
        return None

    suffix = (
        "`"
        if len(ctx.token.text) > 1
        and ctx.next_token is not None
        and ctx.next_token.is_hangul
        else ""
    )
    return RuleResult(ascii_to_dots(f"{encode_number_ascii(ctx.token.text)}{suffix}"))
