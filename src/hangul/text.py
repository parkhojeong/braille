from dataclasses import dataclass

from .decomposition import normalize_print
from .rules.context import RuleContext
from .spans import SpanScanner, TokenSpan
from .tokenization_registry import TOKENIZATION_RULES
from .tokens import Token


def tokenize_normalized_text(normalized_text: str) -> tuple[Token, ...]:
    tokens: list[Token] = []
    group_id = 0
    index = 0

    while index < len(normalized_text):
        for rule in TOKENIZATION_RULES:
            result = rule(normalized_text, index, group_id)
            if result is None:
                continue

            token, index = result
            tokens.append(token)
            if token.is_space:
                group_id += 1
            break

    return tuple(tokens)


def scan_spans(
    tokens: tuple[Token, ...],
    scanners: tuple[SpanScanner, ...],
) -> tuple[TokenSpan, ...]:
    spans: list[TokenSpan] = []
    index = 0

    while index < len(tokens):
        ctx = RuleContext(tokens, index)
        for scanner in scanners:
            span = scanner(ctx)
            if span is None:
                continue

            spans.append(span)
            index = span.end
            break
        else:
            index += 1

    return tuple(spans)


@dataclass(frozen=True)
class Text:
    raw: str
    normalized: str
    tokens: tuple[Token, ...]
    spans: tuple[TokenSpan, ...]

    @classmethod
    def from_print(
        cls,
        raw: str,
        *,
        span_scanners: tuple[SpanScanner, ...] = (),
    ) -> "Text":
        normalized = normalize_print(raw)
        tokens = tokenize_normalized_text(normalized)
        return cls(
            raw=raw,
            normalized=normalized,
            tokens=tokens,
            spans=scan_spans(tokens, span_scanners),
        )

    def context_at(self, index: int) -> RuleContext:
        return RuleContext(self.tokens, index)

    def tokens_for(self, span: TokenSpan) -> tuple[Token, ...]:
        return self.tokens[span.token_slice]

    def text_for(self, span: TokenSpan) -> str:
        return "".join(token.text for token in self.tokens_for(span))

    def span_starting_at(self, index: int) -> TokenSpan | None:
        return next((span for span in self.spans if span.starts_at(index)), None)

    def spans_containing(self, index: int) -> tuple[TokenSpan, ...]:
        return tuple(span for span in self.spans if span.contains(index))

    def previous_token(self, index: int) -> Token | None:
        if index == 0:
            return None
        return self.tokens[index - 1]

    def next_token(self, index: int) -> Token | None:
        if index + 1 >= len(self.tokens):
            return None
        return self.tokens[index + 1]
