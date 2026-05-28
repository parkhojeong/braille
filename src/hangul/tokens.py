from dataclasses import dataclass
from typing import Literal, Optional

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
    group_id: Optional[int] = None
    choseong: Optional[str] = None
    jungseong: Optional[str] = None
    jongseong: Optional[str] = None


PUNCTUATION = {",", ".", "!", "[", "]"}


def tokenize_print(text: str) -> list[Token]:
    normalized_text = normalize_print(text)
    tokens: list[Token] = []
    group_id = 0
    index = 0

    while index < len(normalized_text):
        ch = normalized_text[index]

        if ch.isspace():
            start = index
            while index < len(normalized_text) and normalized_text[index].isspace():
                index += 1
            tokens.append(Token("SPACE", normalized_text[start:index]))
            group_id += 1
            continue

        if ch.isascii() and ch.isalpha():
            start = index
            while (
                index < len(normalized_text)
                and normalized_text[index].isascii()
                and normalized_text[index].isalpha()
            ):
                index += 1
            tokens.append(Token("LATIN_RUN", normalized_text[start:index], group_id))
            continue

        if ch in PUNCTUATION:
            tokens.append(Token("PUNCTUATION", ch, group_id))
            index += 1
            continue

        syllable = decompose_precomposed_hangul_syllable(ch)
        if syllable is not None:
            choseong, jungseong, jongseong = syllable
            tokens.append(
                Token(
                    "HANGUL_SYLLABLE",
                    ch,
                    group_id,
                    choseong=choseong,
                    jungseong=jungseong,
                    jongseong=jongseong,
                )
            )
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
