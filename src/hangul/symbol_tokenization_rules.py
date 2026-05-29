from .character_sets import SYMBOLS
from .tokens import Token

TokenizationResult = tuple[Token, int]


def try_symbol_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    if text[start] not in SYMBOLS:
        return None

    return Token("SYMBOL", text[start], group_id), start + 1
