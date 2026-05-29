from collections.abc import Callable

from .character_sets import (
    PUNCTUATION,
    is_ascii_letter,
    is_compatibility_hangul_jamo,
    is_greek_letter,
)
from .decomposition import decompose_precomposed_hangul_syllable
from .syllables import Syllable
from .tokens import Token

CharPredicate = Callable[[str], bool]
TokenizationResult = tuple[Token, int]


def read_while(text: str, start: int, predicate: CharPredicate) -> int:
    index = start
    while index < len(text) and predicate(text[index]):
        index += 1
    return index


def try_space_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    del group_id
    if not text[start].isspace():
        return None

    end = read_while(text, start, str.isspace)
    return Token("SPACE", text[start:end]), end


def try_latin_run_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    if not is_ascii_letter(text[start]):
        return None

    end = read_while(text, start, is_ascii_letter)
    return Token("LATIN_RUN", text[start:end], group_id), end


def try_greek_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    if not is_greek_letter(text[start]):
        return None

    return Token("GREEK", text[start], group_id), start + 1


def try_punctuation_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    if text[start] not in PUNCTUATION:
        return None

    return Token("PUNCTUATION", text[start], group_id), start + 1


def try_hangul_syllable_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    syllable = decompose_precomposed_hangul_syllable(text[start])
    if syllable is None:
        return None

    l, v, t = syllable
    return (
        Token(
            "HANGUL_SYLLABLE",
            text[start],
            group_id,
            Syllable(l, v, t),
        ),
        start + 1,
    )


def try_jamo_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    if not is_compatibility_hangul_jamo(text[start]):
        return None

    return Token("JAMO", text[start], group_id), start + 1


def try_unknown_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    return Token("UNKNOWN", text[start], group_id), start + 1
