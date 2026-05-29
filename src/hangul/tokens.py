from dataclasses import dataclass
from typing import Literal

from .syllables import Syllable

TokenKind = Literal[
    "GREEK",
    "HANGUL_SYLLABLE",
    "JAMO",
    "LATIN_RUN",
    "NUMBER",
    "SPACE",
    "PUNCTUATION",
    "SYMBOL",
    "UNKNOWN",
]


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    group_id: int | None = None
    syllable: Syllable | None = None

    @property
    def l(self) -> str | None:
        if self.syllable is None:
            return None
        return self.syllable.l

    @property
    def v(self) -> str | None:
        if self.syllable is None:
            return None
        return self.syllable.v

    @property
    def t(self) -> str | None:
        if self.syllable is None:
            return None
        return self.syllable.t

    @property
    def is_hangul(self) -> bool:
        return self.kind == "HANGUL_SYLLABLE"

    @property
    def is_jamo(self) -> bool:
        return self.kind == "JAMO"

    @property
    def is_latin(self) -> bool:
        return self.kind == "LATIN_RUN"

    @property
    def is_greek(self) -> bool:
        return self.kind == "GREEK"

    @property
    def is_number(self) -> bool:
        return self.kind == "NUMBER"

    @property
    def is_space(self) -> bool:
        return self.kind == "SPACE"

    @property
    def is_punctuation(self) -> bool:
        return self.kind == "PUNCTUATION"

    @property
    def is_symbol(self) -> bool:
        return self.kind == "SYMBOL"
