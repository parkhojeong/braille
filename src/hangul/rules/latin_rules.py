from braille.ascii import ascii_to_dots
from ueb.latin_encoder import (
    encode_capital_passage_ascii,
    encode_latin_phrase_run_ascii,
    encode_latin_run_ascii,
)
from ueb.latin_tables import UEB_LATIN_PUNCTUATION_ASCII

from .context import RuleContext, RuleResult
from .latin_phrase import latin_number_phrase_bounds, latin_phrase_bounds
from .number_rules import encode_number_ascii
from .roman_numeral_rules import is_roman_numeral_text


def latin_run_count(ctx: RuleContext) -> int:
    return sum(token.kind == "LATIN_RUN" for token in ctx.tokens)


def is_latin_only_text(ctx: RuleContext) -> bool:
    return all(token.kind in {"LATIN_RUN", "SPACE"} for token in ctx.tokens)


def is_latin_title_or_single_run_text(ctx: RuleContext) -> bool:
    return is_latin_only_text(ctx) and (
        latin_run_count(ctx) == 1
        or all(
            token.kind != "LATIN_RUN" or token.text[0].isupper()
            for token in ctx.tokens
        )
    )


def has_previous_latin_in_phrase(ctx: RuleContext) -> bool:
    index = ctx.index - 1
    while index >= 0 and ctx.tokens[index].kind == "SPACE":
        index -= 1
    return index >= 0 and ctx.tokens[index].kind == "LATIN_RUN"


def has_next_latin_in_phrase(ctx: RuleContext) -> bool:
    index = ctx.index + 1
    while index < len(ctx.tokens) and ctx.tokens[index].kind == "SPACE":
        index += 1
    return index < len(ctx.tokens) and ctx.tokens[index].kind == "LATIN_RUN"


def should_use_latin_indicators(ctx: RuleContext) -> bool:
    if any(token.kind == "GREEK" for token in ctx.tokens):
        return False
    return not is_latin_title_or_single_run_text(ctx)


def should_open_latin_indicator(ctx: RuleContext) -> bool:
    return should_use_latin_indicators(ctx) and not has_previous_latin_in_phrase(ctx)


def should_close_latin_indicator(ctx: RuleContext) -> bool:
    return should_use_latin_indicators(ctx) and not has_next_latin_in_phrase(ctx)


def encode_latin_run(
    text: str,
    *,
    opening_indicator: bool = True,
    closing_indicator: bool = True,
) -> list[str]:
    prefix = "0" if opening_indicator else ""
    suffix = "4" if closing_indicator else ""
    return ascii_to_dots(f"{prefix}{encode_latin_run_ascii(text)}{suffix}")


def is_latin_capital_passage(ctx: RuleContext) -> bool:
    return (
        is_latin_only_text(ctx)
        and latin_run_count(ctx) >= 3
        and all(
            token.kind != "LATIN_RUN" or token.text.isupper()
            for token in ctx.tokens
        )
    )


def encode_latin_capital_passage(ctx: RuleContext) -> RuleResult | None:
    if ctx.index != 0 or not is_latin_capital_passage(ctx):
        return None

    words = [token.text for token in ctx.tokens if token.kind == "LATIN_RUN"]
    return RuleResult(ascii_to_dots(encode_capital_passage_ascii(words)), len(ctx.tokens))


def should_close_latin_phrase(ctx: RuleContext, end: int) -> bool:
    return not (
        ctx.tokens[end - 1].kind == "PUNCTUATION"
        and ctx.tokens[end - 1].text in {".", "!", "?"}
        and end < len(ctx.tokens)
        and ctx.tokens[end].kind == "HANGUL_SYLLABLE"
    )


def encode_latin_phrase_ascii(ctx: RuleContext, start: int, end: int) -> str:
    parts = ["0"]
    for index, token in enumerate(ctx.tokens[start:end], start):
        if token.kind == "LATIN_RUN":
            if index > start and token.text.isupper() and is_roman_numeral_text(
                token.text
            ):
                parts.append(";")
            parts.append(encode_latin_phrase_run_ascii(token.text))
        elif token.kind == "SPACE":
            parts.append("`" * len(token.text))
        elif token.kind == "PUNCTUATION":
            parts.append(UEB_LATIN_PUNCTUATION_ASCII[token.text])
    if should_close_latin_phrase(ctx, end):
        parts.append("4")
    return "".join(parts)


def should_close_latin_number_phrase(ctx: RuleContext, end: int) -> bool:
    return ctx.tokens[end - 1].kind == "LATIN_RUN"


def needs_latin_number_phrase_grade1_indicator(text: str) -> bool:
    return text == "CD"


def encode_latin_number_phrase_ascii(ctx: RuleContext, start: int, end: int) -> str:
    prefix = (
        "`"
        if ctx.previous_token is not None
        and ctx.previous_token.kind == "HANGUL_SYLLABLE"
        else ""
    )
    parts = [f"{prefix}0"]
    for index, token in enumerate(ctx.tokens[start:end], start):
        if token.kind == "LATIN_RUN":
            if (
                index == start
                and needs_latin_number_phrase_grade1_indicator(token.text)
            ):
                parts.append(";")
            parts.append(encode_latin_phrase_run_ascii(token.text))
        elif token.kind == "NUMBER":
            parts.append(encode_number_ascii(token.text))
        elif token.kind == "SPACE":
            parts.append("`" * len(token.text))
        elif token.kind == "SYMBOL" and token.text == "-":
            parts.append("-")

    if should_close_latin_number_phrase(ctx, end):
        parts.append("4")
    return "".join(parts)


def encode_latin(ctx: RuleContext) -> RuleResult | None:
    capital_passage = encode_latin_capital_passage(ctx)
    if capital_passage is not None:
        return capital_passage

    if should_use_latin_indicators(ctx):
        number_phrase = latin_number_phrase_bounds(ctx)
        if number_phrase is not None:
            start, end = number_phrase
            return RuleResult(
                ascii_to_dots(encode_latin_number_phrase_ascii(ctx, start, end)),
                end - start,
            )

        phrase = latin_phrase_bounds(ctx)
        if phrase is not None:
            start, end = phrase
            return RuleResult(
                ascii_to_dots(encode_latin_phrase_ascii(ctx, start, end)),
                end - start,
            )

    if ctx.token.kind != "LATIN_RUN":
        return None

    return RuleResult(
        encode_latin_run(
            ctx.token.text,
            opening_indicator=should_open_latin_indicator(ctx),
            closing_indicator=should_close_latin_indicator(ctx),
        )
    )
