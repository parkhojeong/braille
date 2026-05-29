from braille.ascii import ascii_to_dots

from .context import RuleContext, RuleResult
from .latin_phrase import latin_phrase_bounds
from .latin_tables import (
    UEB_CONTRACTION_ASCII,
    UEB_LATIN_PUNCTUATION_ASCII,
    UEB_SINGLE_LETTER_WORD_INDICATOR_LETTERS,
)


def latin_run_count(ctx: RuleContext) -> int:
    return sum(token.kind == "LATIN_RUN" for token in ctx.tokens)


def is_latin_only_text(ctx: RuleContext) -> bool:
    return all(token.kind in {"LATIN_RUN", "SPACE"} for token in ctx.tokens)


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
    return not (is_latin_only_text(ctx) and latin_run_count(ctx) == 1)


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
    cells: list[str] = ascii_to_dots("0") if opening_indicator else []
    index = 0

    if text and text[0].isupper():
        cells.extend(ascii_to_dots(","))

    lower_text = text.lower()
    while index < len(lower_text):
        for text_part, ascii_part in sorted(
            UEB_CONTRACTION_ASCII.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            if lower_text.startswith(text_part, index):
                cells.extend(ascii_to_dots(ascii_part))
                index += len(text_part)
                break
        else:
            cells.extend(ascii_to_dots(lower_text[index]))
            index += 1

    if closing_indicator:
        cells.extend(ascii_to_dots("4"))
    return cells


def encode_latin_run_ascii(text: str) -> str:
    parts: list[str] = []
    if text and text[0].isupper():
        parts.append(",")
    if len(text) == 1 and text.lower() in UEB_SINGLE_LETTER_WORD_INDICATOR_LETTERS:
        parts.append(";")

    lower_text = text.lower()
    index = 0
    while index < len(lower_text):
        for text_part, ascii_part in sorted(
            UEB_CONTRACTION_ASCII.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            if lower_text.startswith(text_part, index):
                parts.append(ascii_part)
                index += len(text_part)
                break
        else:
            parts.append(lower_text[index])
            index += 1

    return "".join(parts)


def encode_latin_phrase_ascii(ctx: RuleContext, start: int, end: int) -> str:
    parts = ["0"]
    for token in ctx.tokens[start:end]:
        if token.kind == "LATIN_RUN":
            parts.append(encode_latin_run_ascii(token.text))
        elif token.kind == "SPACE":
            parts.append("`" * len(token.text))
        elif token.kind == "PUNCTUATION":
            parts.append(UEB_LATIN_PUNCTUATION_ASCII[token.text])
    parts.append("4")
    return "".join(parts)


def encode_latin(ctx: RuleContext) -> RuleResult | None:
    if should_use_latin_indicators(ctx):
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
