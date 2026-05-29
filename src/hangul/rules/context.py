from dataclasses import dataclass

from ..tokens import Token

SyllableParts = tuple[str, str, str]


@dataclass(frozen=True)
class RuleResult:
    dots: list[str]
    consumed: int = 1


@dataclass(frozen=True)
class RuleContext:
    tokens: list[Token]
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
    def next_syllable(self) -> SyllableParts | None:
        token = self.next_token
        if token is None or token.kind != "HANGUL_SYLLABLE":
            return None

        return token.l or "", token.v or "", token.t or ""

    @property
    def is_group_start(self) -> bool:
        previous_token = self.previous_token
        if previous_token is None:
            return True

        return (
            previous_token.kind in {"SPACE", "PUNCTUATION"}
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
        if any(token.kind != "HANGUL_SYLLABLE" for token in tokens):
            return None

        return "".join(token.text for token in tokens)
