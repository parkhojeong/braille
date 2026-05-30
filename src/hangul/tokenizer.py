from .text import Text
from .tokens import Token


def tokenize_inkprint(text: str) -> list[Token]:
    return list(Text.from_inkprint(text).tokens)
