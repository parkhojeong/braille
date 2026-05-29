from dataclasses import dataclass
from typing import Literal

SpanKind = Literal[
    "LATIN_NUMBER_PHRASE",
    "LATIN_PHRASE",
]


@dataclass(frozen=True)
class TokenSpan:
    kind: SpanKind
    start: int
    end: int
    rule_id: str | None = None

    @property
    def length(self) -> int:
        return self.end - self.start

    @property
    def token_slice(self) -> slice:
        return slice(self.start, self.end)

    def consumed_from(self, index: int) -> int:
        return self.end - index
