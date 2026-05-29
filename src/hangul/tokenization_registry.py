from collections.abc import Callable
from dataclasses import dataclass

from .number_tokenization_rules import try_number_token
from .symbol_tokenization_rules import try_symbol_token
from .tokenization_rules import (
    TokenizationResult,
    try_greek_token,
    try_hangul_syllable_token,
    try_jamo_token,
    try_latin_run_token,
    try_punctuation_token,
    try_space_token,
    try_unknown_token,
)

TokenReader = Callable[[str, int, int], TokenizationResult | None]


@dataclass(frozen=True)
class TokenizationRule:
    name: str
    read: TokenReader


TOKENIZATION_RULES: list[TokenizationRule] = [
    TokenizationRule("space", try_space_token),
    TokenizationRule("number", try_number_token),
    TokenizationRule("latin", try_latin_run_token),
    TokenizationRule("greek", try_greek_token),
    TokenizationRule("punctuation", try_punctuation_token),
    TokenizationRule("symbol", try_symbol_token),
    TokenizationRule("hangul-syllable", try_hangul_syllable_token),
    TokenizationRule("jamo", try_jamo_token),
    TokenizationRule("unknown", try_unknown_token),
]
