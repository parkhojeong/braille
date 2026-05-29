from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .rules.context import RuleContext, RuleResult

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


SpanScanner = Callable[["RuleContext"], TokenSpan | None]
SpanEncoder = Callable[["RuleContext", TokenSpan], str]


@dataclass(frozen=True)
class SpanRule:
    id: str
    scan: SpanScanner
    encode: SpanEncoder


def try_encode_span_rules(
    ctx: "RuleContext",
    rules: list[SpanRule] | tuple[SpanRule, ...],
) -> "RuleResult | None":
    from braille.ascii import ascii_to_dots
    from .rules.context import RuleResult

    for rule in rules:
        span = rule.scan(ctx)
        if span is None:
            continue

        return RuleResult(
            ascii_to_dots(rule.encode(ctx, span)),
            span.consumed_from(ctx.index),
        )
    return None
