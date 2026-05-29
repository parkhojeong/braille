from ueb.latin_tables import UEB_LATIN_PUNCTUATION_ASCII

from ..spans import TokenSpan
from .context import RuleContext
from .symbol_tables import (
    LATIN_HANGUL_BOUNDARY_PUNCTUATION_ASCII,
    LATIN_HANGUL_BOUNDARY_SYMBOL_ASCII,
)

LATIN_PHRASE_TOKEN_KINDS = {"LATIN_RUN", "SPACE", "PUNCTUATION", "SYMBOL"}


def is_latin_phrase_punctuation(text: str) -> bool:
    return text in UEB_LATIN_PUNCTUATION_ASCII


def is_latin_hangul_boundary_mark(ctx: RuleContext, index: int) -> bool:
    token = ctx.tokens[index]
    if token.is_punctuation:
        if token.text not in LATIN_HANGUL_BOUNDARY_PUNCTUATION_ASCII:
            return False
    elif token.is_symbol:
        if token.text not in LATIN_HANGUL_BOUNDARY_SYMBOL_ASCII:
            return False
    else:
        return False

    next_index = index + 1
    while next_index < len(ctx.tokens) and ctx.tokens[next_index].is_space:
        next_index += 1
    return next_index < len(ctx.tokens) and ctx.tokens[next_index].is_hangul


def is_latin_phrase_content_token(ctx: RuleContext, index: int) -> bool:
    token = ctx.tokens[index]
    if token.is_latin:
        return True
    if is_latin_hangul_boundary_mark(ctx, index):
        return True
    return token.is_punctuation and is_latin_phrase_punctuation(token.text)


def can_extend_latin_phrase_left(
    ctx: RuleContext,
    index: int,
    phrase_start: int,
) -> bool:
    if is_latin_phrase_content_token(ctx, index):
        return True
    if (
        ctx.tokens[index].is_space
        and index > 1
        and ctx.tokens[index - 1].is_punctuation
        and not ctx.tokens[index - 2].is_latin
    ):
        return False
    return (
        ctx.tokens[index].is_space
        and index > 0
        and is_latin_phrase_content_token(ctx, index - 1)
        and is_latin_phrase_content_token(ctx, phrase_start)
    )


def can_extend_latin_phrase_right(ctx: RuleContext, index: int) -> bool:
    if is_latin_phrase_content_token(ctx, index):
        return True
    return (
        ctx.tokens[index].is_space
        and index + 1 < len(ctx.tokens)
        and is_latin_phrase_content_token(ctx, index + 1)
    )


def has_latin_run_between(ctx: RuleContext, start: int, end: int) -> bool:
    return any(token.is_latin for token in ctx.tokens[start:end])


def latin_phrase_span(ctx: RuleContext) -> TokenSpan | None:
    if ctx.token.is_space:
        return None
    if (
        (ctx.token.is_punctuation or ctx.token.is_symbol)
        and ctx.next_token is not None
        and ctx.next_token.is_space
    ):
        return None
    if ctx.token.is_punctuation and not is_latin_phrase_punctuation(
        ctx.token.text
    ):
        return None
    if ctx.token.kind not in LATIN_PHRASE_TOKEN_KINDS:
        return None

    start = ctx.index
    while start > 0 and can_extend_latin_phrase_left(ctx, start - 1, start):
        start -= 1

    end = ctx.index + 1
    while end < len(ctx.tokens) and can_extend_latin_phrase_right(ctx, end):
        end += 1

    if start != ctx.index or not has_latin_run_between(ctx, start, end):
        return None
    if end == start + 1:
        return None
    return TokenSpan("LATIN_PHRASE", start, end, "rule-32")


def is_latin_number_phrase_hyphen(ctx: RuleContext, index: int) -> bool:
    token = ctx.tokens[index]
    if not token.is_symbol or token.text != "-":
        return False
    return (
        index > 0
        and ctx.tokens[index - 1].is_latin
        and index + 1 < len(ctx.tokens)
        and ctx.tokens[index + 1].is_number
    )


def can_extend_latin_number_phrase_right(
    ctx: RuleContext,
    index: int,
    saw_number: bool,
) -> bool:
    token = ctx.tokens[index]
    if token.is_number:
        return True
    if token.is_latin:
        return saw_number
    if is_latin_number_phrase_hyphen(ctx, index):
        return True
    return (
        token.is_space
        and index + 1 < len(ctx.tokens)
        and (
            ctx.tokens[index + 1].is_number
            or (saw_number and ctx.tokens[index + 1].is_latin)
        )
    )


def latin_number_phrase_span(ctx: RuleContext) -> TokenSpan | None:
    if not ctx.token.is_latin:
        return None

    end = ctx.index + 1
    saw_number = False
    while end < len(ctx.tokens) and can_extend_latin_number_phrase_right(
        ctx,
        end,
        saw_number,
    ):
        if ctx.tokens[end].is_number:
            saw_number = True
        end += 1

    if not saw_number:
        return None
    return TokenSpan("LATIN_NUMBER_PHRASE", ctx.index, end, "rule-35")
