from dataclasses import dataclass
from typing import Literal

TokenKind = Literal[
    "GREEK",
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
