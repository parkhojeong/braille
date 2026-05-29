import re

from braille.ascii import ascii_to_dots
from ueb.latin_encoder import encode_latin_run_ascii

from .context import RuleContext, RuleResult

ROMAN_NUMERAL_RE = re.compile(r"(?i)^(?:x{0,3})(?:ix|iv|v?i{0,3})$")


def is_roman_numeral_text(text: str) -> bool:
    return bool(text) and bool(ROMAN_NUMERAL_RE.fullmatch(text))


def encode_roman_numeral_ascii(text: str) -> str:
    return f"0{encode_latin_run_ascii(text)}4"


def encode_roman_numeral_range_ascii(start: str, end: str) -> str:
    return f"0{encode_latin_run_ascii(start)}-;{encode_latin_run_ascii(end)}4"


def is_roman_numeral_range_start(ctx: RuleContext) -> bool:
    return (
        ctx.index + 2 < len(ctx.tokens)
        and ctx.tokens[ctx.index + 1].is_symbol
        and ctx.tokens[ctx.index + 1].text == "-"
        and ctx.tokens[ctx.index + 2].is_latin
        and is_roman_numeral_text(ctx.tokens[ctx.index + 2].text)
    )


def should_auto_encode_roman_numeral(ctx: RuleContext) -> bool:
    if is_roman_numeral_range_start(ctx):
        return True
    return ctx.token.text.isupper() and len(ctx.tokens) > 1


def encode_roman_numeral(
    ctx: RuleContext,
    *,
    force: bool = False,
) -> RuleResult | None:
    if not ctx.token.is_latin or not is_roman_numeral_text(ctx.token.text):
        return None
    if not force and not should_auto_encode_roman_numeral(ctx):
        return None

    if is_roman_numeral_range_start(ctx):
        return RuleResult(
            ascii_to_dots(
                encode_roman_numeral_range_ascii(
                    ctx.token.text,
                    ctx.tokens[ctx.index + 2].text,
                )
            ),
            3,
        )

    return RuleResult(ascii_to_dots(encode_roman_numeral_ascii(ctx.token.text)))
