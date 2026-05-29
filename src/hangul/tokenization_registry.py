from collections.abc import Callable

from .tokenization_rules import (
    TokenizationResult,
    try_hangul_syllable_token,
    try_jamo_token,
    try_latin_run_token,
    try_punctuation_token,
    try_space_token,
    try_unknown_token,
)

TokenizationRule = Callable[[str, int, int], TokenizationResult | None]

TOKENIZATION_RULES: list[TokenizationRule] = [
    try_space_token,
    try_latin_run_token,
    try_punctuation_token,
    try_hangul_syllable_token,
    try_jamo_token,
    try_unknown_token,
]
