from .character_sets import is_ascii_digit
from .tokenization_rules import read_while
from .tokens import Token

TokenizationResult = tuple[Token, int]


def try_number_token(
    text: str,
    start: int,
    group_id: int,
) -> TokenizationResult | None:
    if not is_ascii_digit(text[start]):
        return None

    end = read_while(text, start, is_ascii_digit)
    return Token("NUMBER", text[start:end], group_id), end
