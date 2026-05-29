from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from .decomposition import decompose_precomposed_hangul_syllable, normalize_print

TokenKind = Literal[
    "HANGUL_SYLLABLE",
    "JAMO",
    "LATIN_RUN",
    "SPACE",
    "PUNCTUATION",
    "UNKNOWN",
]


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    group_id: int | None = None
    l: str | None = None
    v: str | None = None
    t: str | None = None


PUNCTUATION = {",", ".", "!", "[", "]"}


def is_ascii_letter(ch: str) -> bool:
    return ch.isascii() and ch.isalpha()


CharPredicate = Callable[[str], bool]


def read_while(text: str, start: int, predicate: CharPredicate) -> int:
    index = start
    while index < len(text) and predicate(text[index]):
        index += 1
    return index


def space_token(text: str, start: int) -> tuple[Token, int]:
    end = read_while(text, start, str.isspace)
    return Token("SPACE", text[start:end]), end


def latin_run_token(text: str, start: int, group_id: int) -> tuple[Token, int]:
    end = read_while(text, start, is_ascii_letter)
    return Token("LATIN_RUN", text[start:end], group_id), end


def hangul_syllable_token(ch: str, group_id: int) -> Token | None:
    syllable = decompose_precomposed_hangul_syllable(ch)
    if syllable is None:
        return None

    l, v, t = syllable
    return Token(
        "HANGUL_SYLLABLE",
        ch,
        group_id,
        l=l,
        v=v,
        t=t,
    )


def tokenize_print(text: str) -> list[Token]:
    normalized_text = normalize_print(text)
    tokens: list[Token] = []
    group_id = 0
    index = 0

    while index < len(normalized_text):
        ch = normalized_text[index]

        if ch.isspace():
            token, index = space_token(normalized_text, index)
            tokens.append(token)
            group_id += 1
            continue

        if is_ascii_letter(ch):
            token, index = latin_run_token(normalized_text, index, group_id)
            tokens.append(token)
            continue

        if ch in PUNCTUATION:
            tokens.append(Token("PUNCTUATION", ch, group_id))
            index += 1
            continue

        syllable_token = hangul_syllable_token(ch, group_id)
        if syllable_token is not None:
            tokens.append(syllable_token)
            index += 1
            continue

        if is_compatibility_hangul_jamo(ch):
            tokens.append(Token("JAMO", ch, group_id))
            index += 1
            continue

        tokens.append(Token("UNKNOWN", ch, group_id))
        index += 1

    return tokens


def is_compatibility_hangul_jamo(ch: str) -> bool:
    return "\u3130" <= ch <= "\u318f"
