from .text import Text
from .tokens import Token


def tokenize_print(text: str) -> list[Token]:
    return list(Text.from_print(text).tokens)
