from collections.abc import Callable

from .character_sets import STANDALONE_CONSONANTS
from .rules import (
    RuleContext,
    RuleResult,
    encode_greek,
    encode_jamo,
    encode_latin,
    encode_punctuation,
    encode_syllable,
    encode_vowel_sequence_separator,
    encode_word,
)
from .tokens import Token

TokenPhase = Callable[[RuleContext, str], RuleResult | None]


def should_skip_space(ctx: RuleContext) -> bool:
    if ctx.previous_token is None or ctx.next_token is None:
        return False

    return (
        ctx.token.text == " "
        and ctx.previous_token.kind == "JAMO"
        and ctx.previous_token.text in STANDALONE_CONSONANTS
        and ctx.next_token.kind == "HANGUL_SYLLABLE"
        and ctx.next_token.text == "자"
    )


def encode_next_syllable_separator(tokens: list[Token], index: int) -> list[str]:
    if index + 1 >= len(tokens):
        return []

    token = tokens[index]
    next_token = tokens[index + 1]
    if token.kind != "HANGUL_SYLLABLE" or next_token.kind != "HANGUL_SYLLABLE":
        return []

    return encode_vowel_sequence_separator(
        token.v or "",
        token.t or "",
        next_token.l or "",
        next_token.v or "",
        next_token.t or "",
    )


def encode_word_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_word(ctx)


def encode_latin_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_latin(ctx)


def encode_greek_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_greek(ctx)


def encode_space_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    if ctx.token.kind != "SPACE":
        return None

    if should_skip_space(ctx):
        return RuleResult([])
    return RuleResult([""] * len(ctx.token.text))


def encode_punctuation_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_punctuation(ctx)


def encode_hangul_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    if ctx.token.kind != "HANGUL_SYLLABLE":
        return None

    dots = [
        *encode_syllable(ctx),
        *encode_next_syllable_separator(ctx.tokens, ctx.index),
    ]
    return RuleResult(dots)


def encode_jamo_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    if ctx.token.kind != "JAMO":
        return None
    return RuleResult(encode_jamo(ctx.token.text, jamo_role))


TOKEN_PHASES: list[TokenPhase] = [
    encode_word_phase,
    encode_latin_phase,
    encode_greek_phase,
    encode_space_phase,
    encode_punctuation_phase,
    encode_hangul_phase,
    encode_jamo_phase,
]
