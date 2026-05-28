from braille.ascii import dots_to_ascii

from .decomposition import decompose_precomposed_hangul_syllable, normalize_print
from .rules import encode_standalone_jamo, encode_syllable


def print_to_braille_dots(text: str, *, standalone_jamo: str = "choseong") -> list[str]:
    result: list[str] = []

    for ch in normalize_print(text):
        syllable = decompose_precomposed_hangul_syllable(ch)
        if syllable is not None:
            result.extend(encode_syllable(*syllable))
            continue

        result.extend(encode_standalone_jamo(ch, standalone_jamo))

    return result


def print_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(print_to_braille_dots(text))
