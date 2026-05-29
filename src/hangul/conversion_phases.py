from collections.abc import Callable, Sequence
from dataclasses import dataclass

from .character_sets import STANDALONE_CONSONANTS
from .rules import (
    RuleContext,
    RuleResult,
    encode_greek,
    encode_jamo,
    encode_latin,
    encode_number,
    encode_punctuation,
    encode_roman_numeral,
    encode_syllable,
    encode_vowel_sequence_separator,
    encode_word,
)
from .tokens import Token

TokenPhaseEncoder = Callable[[RuleContext, str], RuleResult | None]


@dataclass(frozen=True)
class TokenPhase:
    name: str
    encode: TokenPhaseEncoder


def should_skip_space(ctx: RuleContext) -> bool:
    if ctx.previous_token is None or ctx.next_token is None:
        return False

    return (
        ctx.token.text == " "
        and ctx.previous_token.is_jamo
        and ctx.previous_token.text in STANDALONE_CONSONANTS
        and ctx.next_token.is_hangul
        and ctx.next_token.text == "자"
    )


def encode_next_syllable_separator(tokens: Sequence[Token], index: int) -> list[str]:
    if index + 1 >= len(tokens):
        return []

    token = tokens[index]
    next_token = tokens[index + 1]
    if not token.is_hangul or not next_token.is_hangul:
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


def encode_roman_numeral_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    return encode_roman_numeral(ctx, force=jamo_role == "roman_numeral")


def encode_greek_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_greek(ctx)


def encode_number_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_number(ctx)


def encode_space_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    if not ctx.token.is_space:
        return None

    if should_skip_space(ctx):
        return RuleResult([])
    return RuleResult([""] * len(ctx.token.text))


def encode_punctuation_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    return encode_punctuation(ctx)


def encode_hangul_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    del jamo_role
    if not ctx.token.is_hangul:
        return None

    dots = [
        *encode_syllable(ctx),
        *encode_next_syllable_separator(ctx.tokens, ctx.index),
    ]
    return RuleResult(dots)


def encode_jamo_phase(ctx: RuleContext, jamo_role: str) -> RuleResult | None:
    if not ctx.token.is_jamo:
        return None
    return RuleResult(encode_jamo(ctx.token.text, jamo_role))


TOKEN_PHASES: list[TokenPhase] = [
    TokenPhase("word", encode_word_phase),
    TokenPhase("roman-numeral", encode_roman_numeral_phase),
    TokenPhase("latin", encode_latin_phase),
    TokenPhase("greek", encode_greek_phase),
    TokenPhase("number", encode_number_phase),
    TokenPhase("space", encode_space_phase),
    TokenPhase("punctuation", encode_punctuation_phase),
    TokenPhase("hangul", encode_hangul_phase),
    TokenPhase("jamo", encode_jamo_phase),
]
