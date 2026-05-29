from .greek_tables import GREEK_ASCII


def is_uppercase_greek(ch: str) -> bool:
    return ch in GREEK_ASCII and ch.upper() == ch and ch.lower() != ch


def encode_greek_ascii(
    text: str,
    *,
    previous_is_uppercase: bool = False,
    next_is_uppercase: bool = False,
) -> str:
    ascii_text = GREEK_ASCII[text]
    if not is_uppercase_greek(text):
        return ascii_text

    base_ascii = ascii_text.removeprefix(",")
    if previous_is_uppercase:
        return base_ascii
    if next_is_uppercase:
        return f",{ascii_text}"
    return ascii_text
