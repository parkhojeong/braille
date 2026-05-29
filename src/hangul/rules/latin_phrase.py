from .context import RuleContext
from ueb.latin_tables import UEB_LATIN_PUNCTUATION_ASCII

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


def latin_phrase_bounds(ctx: RuleContext) -> tuple[int, int] | None:
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
    return start, end
