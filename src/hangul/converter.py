from braille.ascii import dots_to_ascii

from .conversion_phases import TOKEN_PHASES
from .rules.latin_phrase import latin_number_phrase_span, latin_phrase_span
from .rules import RuleContext, RuleResult
from .text import Text

TEXT_SPAN_SCANNERS = (
    latin_number_phrase_span,
    latin_phrase_span,
)


def encode_token(ctx: RuleContext, jamo_role: str) -> RuleResult:
    for phase in TOKEN_PHASES:
        result = phase(ctx, jamo_role)
        if result is not None:
            return result

    raise NotImplementedError(f"unsupported token: {ctx.token.text}")


def print_to_braille_dots(text: str, *, jamo_role: str = "l") -> list[str]:
    result: list[str] = []
    braille_text = Text.from_print(text, span_scanners=TEXT_SPAN_SCANNERS)
    index = 0

    while index < len(braille_text.tokens):
        encoded = encode_token(braille_text.context_at(index), jamo_role)
        result.extend(encoded.dots)
        index += encoded.consumed

    return result


def print_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(print_to_braille_dots(text))
