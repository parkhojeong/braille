from braille.ascii import ascii_to_dots, dots_to_ascii

from .rules import encode_jamo, encode_syllable, encode_vowel_sequence_separator
from .tokens import Token, tokenize_print

TEXT_PUNCTUATION_DOTS = {
    " ": [""],
    ",": ["5"],
    ".": ["256"],
    "!": ["2346"],
    "[": ["236", "23"],
    "]": ["56", "356"],
}

STANDALONE_CONSONANTS = {
    "ㄱ",
    "ㄴ",
    "ㄷ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅅ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
}


def encode_latin_run(text: str) -> list[str]:
    cells: list[str] = ascii_to_dots("0")
    index = 0

    if text and text[0].isupper():
        cells.extend(ascii_to_dots(","))

    lower_text = text.lower()
    while index < len(lower_text):
        if lower_text[index : index + 2] == "ar":
            cells.extend(ascii_to_dots(">"))
            index += 2
            continue

        cells.extend(ascii_to_dots(lower_text[index]))
        index += 1

    cells.extend(TEXT_PUNCTUATION_DOTS["."])
    return cells


def should_skip_space(tokens: list[Token], index: int) -> bool:
    if index == 0 or index + 1 >= len(tokens):
        return False

    previous_token = tokens[index - 1]
    next_token = tokens[index + 1]
    return (
        tokens[index].text == " "
        and previous_token.kind == "JAMO"
        and previous_token.text in STANDALONE_CONSONANTS
        and next_token.kind == "HANGUL_SYLLABLE"
        and next_token.text == "자"
    )


def next_syllable_l_is_ㅇ(tokens: list[Token], index: int) -> bool:
    if index + 1 >= len(tokens):
        return False

    next_token = tokens[index + 1]
    return next_token.kind == "HANGUL_SYLLABLE" and next_token.l == "ㅇ"


def encode_next_syllable_separator(tokens: list[Token], index: int) -> list[str]:
    if index + 1 >= len(tokens):
        return []

    token = tokens[index]
    next_token = tokens[index + 1]
    if token.kind != "HANGUL_SYLLABLE" or next_token.kind != "HANGUL_SYLLABLE":
        return []

    return encode_vowel_sequence_separator(
        token.v or "",
        token.t or "",
        next_token.l or "",
        next_token.v or "",
        next_token.t or "",
    )


def print_to_braille_dots(text: str, *, jamo_role: str = "l") -> list[str]:
    result: list[str] = []
    tokens = tokenize_print(text)

    for index, token in enumerate(tokens):
        if token.kind == "SPACE" and should_skip_space(tokens, index):
            continue

        if token.kind == "LATIN_RUN":
            result.extend(encode_latin_run(token.text))
            continue

        if token.kind == "SPACE":
            result.extend([""] * len(token.text))
            continue

        if token.kind == "PUNCTUATION":
            result.extend(TEXT_PUNCTUATION_DOTS[token.text])
            continue

        if token.kind == "HANGUL_SYLLABLE":
            result.extend(
                encode_syllable(
                    token.l or "",
                    token.v or "",
                    token.t or "",
                    next_syllable_l_is_ㅇ=next_syllable_l_is_ㅇ(
                        tokens, index
                    ),
                )
            )
            result.extend(encode_next_syllable_separator(tokens, index))
            continue

        result.extend(encode_jamo(token.text, jamo_role))

    return result


def print_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(print_to_braille_dots(text))
