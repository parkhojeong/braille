from braille.ascii import ascii_to_dots, dots_to_ascii

from .decomposition import decompose_precomposed_hangul_syllable, normalize_print
from .rules import encode_standalone_jamo, encode_syllable

TEXT_PUNCTUATION_DOTS = {
    " ": [""],
    ",": ["5"],
    ".": ["256"],
    "!": ["2346"],
    "[": ["236", "23"],
    "]": ["56", "356"],
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


def print_to_braille_dots(text: str, *, standalone_jamo: str = "choseong") -> list[str]:
    result: list[str] = []
    text = normalize_print(text)
    index = 0

    while index < len(text):
        ch = text[index]

        if (
            ch == " "
            and index > 0
            and index + 1 < len(text)
            and text[index + 1] == "자"
            and text[index - 1] in {
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
        ):
            index += 1
            continue

        if ch.isascii() and ch.isalpha():
            start = index
            while index < len(text) and text[index].isascii() and text[index].isalpha():
                index += 1
            result.extend(encode_latin_run(text[start:index]))
            continue

        if ch in TEXT_PUNCTUATION_DOTS:
            result.extend(TEXT_PUNCTUATION_DOTS[ch])
            index += 1
            continue

        syllable = decompose_precomposed_hangul_syllable(ch)
        if syllable is not None:
            next_syllable = (
                decompose_precomposed_hangul_syllable(text[index + 1])
                if index + 1 < len(text)
                else None
            )
            result.extend(
                encode_syllable(
                    *syllable,
                    next_syllable_starts_with_ieung=(
                        next_syllable is not None and next_syllable[0] == "ㅇ"
                    ),
                )
            )
            index += 1
            continue

        result.extend(encode_standalone_jamo(ch, standalone_jamo))
        index += 1

    return result


def print_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(print_to_braille_dots(text))
