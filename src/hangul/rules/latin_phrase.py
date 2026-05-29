from ueb.latin_tables import UEB_LATIN_PUNCTUATION_ASCII

from ..spans import TokenSpan
from .context import RuleContext

LATIN_PHRASE_TOKEN_KINDS = {"LATIN_RUN", "SPACE", "PUNCTUATION"}


def is_latin_phrase_punctuation(text: str) -> bool:
    return text in UEB_LATIN_PUNCTUATION_ASCII


def is_latin_phrase_content_token(ctx: RuleContext, index: int) -> bool:
    token = ctx.tokens[index]
    if token.kind == "LATIN_RUN":
        return True
    return token.kind == "PUNCTUATION" and is_latin_phrase_punctuation(token.text)


def can_extend_latin_phrase_left(
    ctx: RuleContext,
    index: int,
    phrase_start: int,
) -> bool:
    if is_latin_phrase_content_token(ctx, index):
        return True
    return (
        ctx.tokens[index].kind == "SPACE"
        and index > 0
        and is_latin_phrase_content_token(ctx, index - 1)
        and is_latin_phrase_content_token(ctx, phrase_start)
    )


def can_extend_latin_phrase_right(ctx: RuleContext, index: int) -> bool:
    if is_latin_phrase_content_token(ctx, index):
        return True
    return (
        ctx.tokens[index].kind == "SPACE"
        and index + 1 < len(ctx.tokens)
        and is_latin_phrase_content_token(ctx, index + 1)
    )


def has_latin_run_between(ctx: RuleContext, start: int, end: int) -> bool:
    return any(token.kind == "LATIN_RUN" for token in ctx.tokens[start:end])


def latin_phrase_span(ctx: RuleContext) -> TokenSpan | None:
    if ctx.token.kind == "SPACE":
        return None
    if ctx.token.kind == "PUNCTUATION" and not is_latin_phrase_punctuation(
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
    return TokenSpan("LATIN_PHRASE", start, end, "rule-32")


def is_latin_number_phrase_hyphen(ctx: RuleContext, index: int) -> bool:
    token = ctx.tokens[index]
    if token.kind != "SYMBOL" or token.text != "-":
        return False
    return (
        index > 0
        and ctx.tokens[index - 1].kind == "LATIN_RUN"
        and index + 1 < len(ctx.tokens)
        and ctx.tokens[index + 1].kind == "NUMBER"
    )


def can_extend_latin_number_phrase_right(
    ctx: RuleContext,
    index: int,
    saw_number: bool,
) -> bool:
    token = ctx.tokens[index]
    if token.kind == "NUMBER":
        return True
    if token.kind == "LATIN_RUN":
        return saw_number
    if is_latin_number_phrase_hyphen(ctx, index):
        return True
    return (
        token.kind == "SPACE"
        and index + 1 < len(ctx.tokens)
        and (
            ctx.tokens[index + 1].kind == "NUMBER"
            or (saw_number and ctx.tokens[index + 1].kind == "LATIN_RUN")
        )
    )


def latin_number_phrase_span(ctx: RuleContext) -> TokenSpan | None:
    if ctx.token.kind != "LATIN_RUN":
        return None

    end = ctx.index + 1
    saw_number = False
    while end < len(ctx.tokens) and can_extend_latin_number_phrase_right(
        ctx,
        end,
        saw_number,
    ):
        if ctx.tokens[end].kind == "NUMBER":
            saw_number = True
        end += 1

    if not saw_number:
        return None
    return TokenSpan("LATIN_NUMBER_PHRASE", ctx.index, end, "rule-35")
