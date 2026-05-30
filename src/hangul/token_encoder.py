from .conversion_phases import TOKEN_PHASES
from .line_aware_encoder import try_encode_line_aware_token
from .rules import RuleContext, RuleResult
from .rules.latin_phrase import latin_number_phrase_span, latin_phrase_span
from .text import Text

TEXT_SPAN_SCANNERS = (
    latin_number_phrase_span,
    latin_phrase_span,
)


def encode_token_context(ctx: RuleContext, jamo_role: str) -> RuleResult:
    for phase in TOKEN_PHASES:
        result = phase.encode(ctx, jamo_role)
        if result is not None:
            return result

    raise NotImplementedError(f"unsupported token: {ctx.token.text}")


def encode_text_to_dots(
    text: Text,
    *,
    jamo_role: str = "l",
    line_width: int | None = None,
    initial_line_position: int = 0,
) -> list[str]:
    result: list[str] = []
    index = 0
    line_position = initial_line_position

    while index < len(text.tokens):
        ctx = text.context_at(index)
        encoded = None
        if line_width is not None:
            encoded = try_encode_line_aware_token(
                ctx,
                braille_text=text,
                jamo_role=jamo_role,
                line_width=line_width,
                line_position=line_position,
                encode_token=encode_token_context,
            )
        if encoded is None:
            encoded = encode_token_context(ctx, jamo_role)

        result.extend(encoded.dots)
        if line_width is not None:
            line_position = (line_position + len(encoded.dots)) % line_width
        index += encoded.consumed

    return result


def encode_print_text_to_dots(
    print_text: str,
    *,
    jamo_role: str = "l",
    line_width: int | None = None,
    initial_line_position: int = 0,
) -> list[str]:
    text = Text.from_print(print_text, span_scanners=TEXT_SPAN_SCANNERS)
    return encode_text_to_dots(
        text,
        jamo_role=jamo_role,
        line_width=line_width,
        initial_line_position=initial_line_position,
    )
