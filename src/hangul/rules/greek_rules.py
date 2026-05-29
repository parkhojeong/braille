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


def is_in_korean_sentence(ctx: RuleContext) -> bool:
    return any(token.kind == "HANGUL_SYLLABLE" for token in ctx.tokens)


def is_greek_run_start(ctx: RuleContext) -> bool:
    return ctx.previous_token is None or ctx.previous_token.kind != "GREEK"


def is_greek_run_end(ctx: RuleContext) -> bool:
    return ctx.next_token is None or ctx.next_token.kind != "GREEK"


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

    ascii_text = encode_greek_ascii(ctx)
    if is_in_korean_sentence(ctx):
        if is_greek_run_start(ctx):
            ascii_text = f"0{ascii_text}"
        if is_greek_run_end(ctx):
            ascii_text = f"{ascii_text}4"

    return RuleResult(ascii_to_dots(ascii_text))
