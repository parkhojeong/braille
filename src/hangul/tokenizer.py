from .decomposition import normalize_print
from .tokenization_registry import TOKENIZATION_RULES
from .tokens import Token


def tokenize_print(text: str) -> list[Token]:
    normalized_text = normalize_print(text)
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
            if token.kind == "SPACE":
                group_id += 1
            break

    return tokens
