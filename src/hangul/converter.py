from braille.ascii import dots_to_ascii

from .conversion_phases import TOKEN_PHASES
from .rules import RuleContext, RuleResult
from .tokens import tokenize_print


def encode_token(ctx: RuleContext, jamo_role: str) -> RuleResult:
    for phase in TOKEN_PHASES:
        result = phase(ctx, jamo_role)
        if result is not None:
            return result

    raise NotImplementedError(f"unsupported token: {ctx.token.text}")


def print_to_braille_dots(text: str, *, jamo_role: str = "l") -> list[str]:
    result: list[str] = []
    tokens = tokenize_print(text)
    index = 0

    while index < len(tokens):
        encoded = encode_token(RuleContext(tokens, index), jamo_role)
        result.extend(encoded.dots)
        index += encoded.consumed

    return result


def print_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(print_to_braille_dots(text))
