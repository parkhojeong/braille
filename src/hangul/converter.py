from braille.ascii import ascii_to_dots, dots_to_ascii

from .rules import encode_jamo, encode_syllable, encode_vowel_sequence_separator
from .tokens import Token, tokenize_print

TEXT_PUNCTUATION_DOTS = {
    " ": [""],
    ",": ["5"],
    ".": ["256"],
    "!": ["2346"],
    "?": ["236"],
    "[": ["236", "23"],
    "]": ["56", "356"],
}

WORD_ABBREVIATION_DOTS = {
    "그래서": ascii_to_dots("as"),
    "그러나": ascii_to_dots("ac"),
    "그러면": ascii_to_dots("a3"),
    "그러므로": ascii_to_dots("a5"),
    "그런데": ascii_to_dots("an"),
    "그리고": ascii_to_dots("au"),
    "그리하여": ascii_to_dots("a:"),
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


def next_syllable_parts(tokens: list[Token], index: int) -> tuple[str, str, str] | None:
    if index + 1 >= len(tokens):
        return None

    next_token = tokens[index + 1]
    if next_token.kind != "HANGUL_SYLLABLE":
        return None

    return next_token.l or "", next_token.v or "", next_token.t or ""


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


def is_group_start(tokens: list[Token], index: int) -> bool:
    if index == 0:
        return True

    previous_token = tokens[index - 1]
    return (
        previous_token.kind in {"SPACE", "PUNCTUATION"}
        or previous_token.group_id != tokens[index].group_id
    )


def previous_group_text(tokens: list[Token], index: int) -> str:
    group_id = tokens[index].group_id
    start = index
    while start > 0 and tokens[start - 1].group_id == group_id:
        start -= 1
    return "".join(token.text for token in tokens[start:index])


def try_encode_word_abbreviation(
    tokens: list[Token],
    index: int,
) -> tuple[list[str], int] | None:
    prefix_dots: list[str] = []
    if not is_group_start(tokens, index):
        if previous_group_text(tokens, index) != "왜":
            return None
        prefix_dots = [""]

    for word, dots in sorted(
        WORD_ABBREVIATION_DOTS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        end = index + len(word)
        if end > len(tokens):
            continue

        word_tokens = tokens[index:end]
        if any(token.kind != "HANGUL_SYLLABLE" for token in word_tokens):
            continue

        if "".join(token.text for token in word_tokens) == word:
            return [*prefix_dots, *dots], len(word)

    return None


def print_to_braille_dots(text: str, *, jamo_role: str = "l") -> list[str]:
    result: list[str] = []
    tokens = tokenize_print(text)
    index = 0

    while index < len(tokens):
        token = tokens[index]
        if token.kind == "SPACE" and should_skip_space(tokens, index):
            index += 1
            continue

        if token.kind == "LATIN_RUN":
            result.extend(encode_latin_run(token.text))
            index += 1
            continue

        if token.kind == "SPACE":
            result.extend([""] * len(token.text))
            index += 1
            continue

        if token.kind == "PUNCTUATION":
            result.extend(TEXT_PUNCTUATION_DOTS[token.text])
            index += 1
            continue

        if token.kind == "HANGUL_SYLLABLE":
            abbreviation = try_encode_word_abbreviation(tokens, index)
            if abbreviation is not None:
                dots, consumed = abbreviation
                result.extend(dots)
                index += consumed
                continue

            result.extend(
                encode_syllable(
                    token.l or "",
                    token.v or "",
                    token.t or "",
                    next_syllable=next_syllable_parts(tokens, index),
                )
            )
            result.extend(encode_next_syllable_separator(tokens, index))
            index += 1
            continue

        result.extend(encode_jamo(token.text, jamo_role))
        index += 1

    return result


def print_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(print_to_braille_dots(text))
