from braille.ascii import ascii_to_dots

from .context import RuleContext, RuleResult
from .greek_tables import GREEK_ASCII


def is_uppercase_greek(ch: str) -> bool:
    return ch in GREEK_ASCII and ch.upper() == ch and ch.lower() != ch


def has_previous_uppercase_greek(ctx: RuleContext) -> bool:
    return (
        ctx.index > 0
        and ctx.tokens[ctx.index - 1].kind == "GREEK"
        and is_uppercase_greek(ctx.tokens[ctx.index - 1].text)
    )


def has_next_uppercase_greek(ctx: RuleContext) -> bool:
    return (
        ctx.index + 1 < len(ctx.tokens)
        and ctx.tokens[ctx.index + 1].kind == "GREEK"
        and is_uppercase_greek(ctx.tokens[ctx.index + 1].text)
    )


def encode_greek_ascii(ctx: RuleContext) -> str:
    ascii_text = GREEK_ASCII[ctx.token.text]
    if not is_uppercase_greek(ctx.token.text):
        return ascii_text

    base_ascii = ascii_text.removeprefix(",")
    if has_previous_uppercase_greek(ctx):
        return base_ascii
    if has_next_uppercase_greek(ctx):
        return f",{ascii_text}"
    return ascii_text


def encode_greek(ctx: RuleContext) -> RuleResult | None:
    if ctx.token.kind != "GREEK":
        return None

    return RuleResult(ascii_to_dots(encode_greek_ascii(ctx)))
