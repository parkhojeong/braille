from braille.ascii import ascii_to_dots
from ueb.latin_encoder import (
    encode_capital_passage_ascii,
    encode_latin_phrase_run_ascii,
    encode_latin_run_ascii,
)
from ueb.latin_tables import UEB_LATIN_PUNCTUATION_ASCII

from ..spans import SpanRule, TokenSpan, try_encode_span_rules
from .context import RuleContext, RuleResult
from .latin_phrase import (
    is_latin_hangul_boundary_mark,
    latin_number_phrase_span,
    latin_phrase_span,
)
from .number_rules import encode_number_ascii
from .roman_numeral_rules import is_roman_numeral_text
from .symbol_tables import (
    LATIN_HANGUL_BOUNDARY_PUNCTUATION_ASCII,
    LATIN_HANGUL_BOUNDARY_SYMBOL_ASCII,
)


def latin_run_count(ctx: RuleContext) -> int:
    return sum(token.is_latin for token in ctx.tokens)


def is_latin_only_text(ctx: RuleContext) -> bool:
    return all(token.is_latin or token.is_space for token in ctx.tokens)


def is_latin_title_or_single_run_text(ctx: RuleContext) -> bool:
    return is_latin_only_text(ctx) and (
        latin_run_count(ctx) == 1
        or all(
            not token.is_latin or token.text[0].isupper()
            for token in ctx.tokens
        )
    )


def has_previous_latin_in_phrase(ctx: RuleContext) -> bool:
    index = ctx.index - 1
    while index >= 0 and ctx.tokens[index].is_space:
        index -= 1
    return index >= 0 and ctx.tokens[index].is_latin


def has_next_latin_in_phrase(ctx: RuleContext) -> bool:
    index = ctx.index + 1
    while index < len(ctx.tokens) and ctx.tokens[index].is_space:
        index += 1
    return index < len(ctx.tokens) and ctx.tokens[index].is_latin


def should_use_latin_indicators(ctx: RuleContext) -> bool:
    if any(token.is_greek for token in ctx.tokens):
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
        and all(not token.is_latin or token.text.isupper() for token in ctx.tokens)
    )


def encode_latin_capital_passage(ctx: RuleContext) -> RuleResult | None:
    if ctx.index != 0 or not is_latin_capital_passage(ctx):
        return None

    words = [token.text for token in ctx.tokens if token.is_latin]
    return RuleResult(ascii_to_dots(encode_capital_passage_ascii(words)), len(ctx.tokens))


def should_close_latin_phrase(ctx: RuleContext, span: TokenSpan) -> bool:
    end_token = ctx.tokens[span.end - 1]
    if is_latin_hangul_boundary_mark(ctx, span.end - 1):
        return False

    return not (
        end_token.is_punctuation
        and end_token.text in {".", "!", "?"}
        and span.end < len(ctx.tokens)
        and ctx.tokens[span.end].is_hangul
    )


def encode_latin_phrase_ascii(ctx: RuleContext, span: TokenSpan) -> str:
    parts = ["0"]
    for index, token in enumerate(ctx.tokens[span.token_slice], span.start):
        if token.is_latin:
            if (
                index > span.start
                and token.text.isupper()
                and is_roman_numeral_text(token.text)
            ):
                parts.append(";")
            parts.append(encode_latin_phrase_run_ascii(token.text))
        elif token.is_space:
            parts.append("`" * len(token.text))
        elif token.is_punctuation:
            boundary_ascii = None
            if is_latin_hangul_boundary_mark(ctx, index):
                boundary_ascii = LATIN_HANGUL_BOUNDARY_PUNCTUATION_ASCII.get(
                    token.text
                )
            if boundary_ascii is not None:
                parts.append(boundary_ascii)
            else:
                parts.append(UEB_LATIN_PUNCTUATION_ASCII[token.text])
        elif token.is_symbol:
            parts.append(LATIN_HANGUL_BOUNDARY_SYMBOL_ASCII[token.text])
    if should_close_latin_phrase(ctx, span):
        parts.append("4")
    return "".join(parts)


def should_close_latin_number_phrase(ctx: RuleContext, span: TokenSpan) -> bool:
    return ctx.tokens[span.end - 1].is_latin


def needs_latin_number_phrase_grade1_indicator(text: str) -> bool:
    return text == "CD"


def encode_latin_number_phrase_ascii(ctx: RuleContext, span: TokenSpan) -> str:
    prefix = (
        "`"
        if ctx.previous_token is not None
        and ctx.previous_token.is_hangul
        else ""
    )
    parts = [f"{prefix}0"]
    for index, token in enumerate(ctx.tokens[span.token_slice], span.start):
        if token.is_latin:
            if (
                index == span.start
                and needs_latin_number_phrase_grade1_indicator(token.text)
            ):
                parts.append(";")
            parts.append(encode_latin_phrase_run_ascii(token.text))
        elif token.is_number:
            parts.append(encode_number_ascii(token.text))
        elif token.is_space:
            parts.append("`" * len(token.text))
        elif token.is_symbol and token.text == "-":
            parts.append("-")

    if should_close_latin_number_phrase(ctx, span):
        parts.append("4")
    return "".join(parts)


LATIN_SPAN_RULES = [
    SpanRule("rule-35", latin_number_phrase_span, encode_latin_number_phrase_ascii),
    SpanRule("rule-32", latin_phrase_span, encode_latin_phrase_ascii),
]


def encode_latin(ctx: RuleContext) -> RuleResult | None:
    capital_passage = encode_latin_capital_passage(ctx)
    if capital_passage is not None:
        return capital_passage

    if should_use_latin_indicators(ctx):
        span_result = try_encode_span_rules(ctx, LATIN_SPAN_RULES)
        if span_result is not None:
            return span_result

    if not ctx.token.is_latin:
        return None

    return RuleResult(
        encode_latin_run(
            ctx.token.text,
            opening_indicator=should_open_latin_indicator(ctx),
            closing_indicator=should_close_latin_indicator(ctx),
        )
    )
