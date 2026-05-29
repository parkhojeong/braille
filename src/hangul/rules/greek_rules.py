from braille.ascii import ascii_to_dots
from ueb.greek_encoder import encode_greek_ascii, is_uppercase_greek

from .context import RuleContext, RuleResult


def has_previous_uppercase_greek(ctx: RuleContext) -> bool:
    return (
        ctx.index > 0
        and ctx.tokens[ctx.index - 1].is_greek
        and is_uppercase_greek(ctx.tokens[ctx.index - 1].text)
    )


def has_next_uppercase_greek(ctx: RuleContext) -> bool:
    return (
        ctx.index + 1 < len(ctx.tokens)
        and ctx.tokens[ctx.index + 1].is_greek
        and is_uppercase_greek(ctx.tokens[ctx.index + 1].text)
    )


def is_in_korean_sentence(ctx: RuleContext) -> bool:
    return any(token.is_hangul for token in ctx.tokens)


def is_greek_run_start(ctx: RuleContext) -> bool:
    return ctx.previous_token is None or not ctx.previous_token.is_greek


def is_greek_run_end(ctx: RuleContext) -> bool:
    return ctx.next_token is None or not ctx.next_token.is_greek


def encode_greek(ctx: RuleContext) -> RuleResult | None:
    if not ctx.token.is_greek:
        return None

    ascii_text = encode_greek_ascii(
        ctx.token.text,
        previous_is_uppercase=has_previous_uppercase_greek(ctx),
        next_is_uppercase=has_next_uppercase_greek(ctx),
    )
    if is_in_korean_sentence(ctx):
        if is_greek_run_start(ctx):
            ascii_text = f"0{ascii_text}"
        if is_greek_run_end(ctx):
            ascii_text = f"{ascii_text}4"

    return RuleResult(ascii_to_dots(ascii_text))
