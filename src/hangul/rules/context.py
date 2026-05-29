from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..tokens import Token
from ..syllables import Syllable

if TYPE_CHECKING:
    from ..spans import TokenSpan

@dataclass(frozen=True)
class RuleResult:
    dots: list[str]
    consumed: int = 1
    rule_id: str | None = None
    span: "TokenSpan | None" = None


@dataclass(frozen=True)
class RuleContext:
    tokens: Sequence[Token]
    index: int

    @property
    def token(self) -> Token:
        return self.tokens[self.index]

    @property
    def previous_token(self) -> Token | None:
        if self.index == 0:
            return None
        return self.tokens[self.index - 1]

    @property
    def next_token(self) -> Token | None:
        if self.index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.index + 1]

    @property
    def syllable(self) -> Syllable:
        return self.token.syllable_or_empty

    @property
    def next_syllable(self) -> Syllable | None:
        token = self.next_token
        if token is None or not token.is_hangul:
            return None

        return token.syllable

    @property
    def l(self) -> str:
        return self.syllable.l

    @property
    def v(self) -> str:
        return self.syllable.v

    @property
    def t(self) -> str:
        return self.syllable.t

    @property
    def is_group_start(self) -> bool:
        previous_token = self.previous_token
        if previous_token is None:
            return True

        return (
            previous_token.is_space
            or previous_token.is_punctuation
            or previous_token.group_id != self.token.group_id
        )

    @property
    def previous_group_text(self) -> str:
        group_id = self.token.group_id
        start = self.index
        while start > 0 and self.tokens[start - 1].group_id == group_id:
            start -= 1
        return "".join(token.text for token in self.tokens[start : self.index])

    def text_from_current(self, length: int) -> str | None:
        end = self.index + length
        if end > len(self.tokens):
            return None

        tokens = self.tokens[self.index:end]
        if any(not token.is_hangul for token in tokens):
            return None

        return "".join(token.text for token in tokens)
