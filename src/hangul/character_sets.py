PUNCTUATION = {",", ".", "!", "?", "[", "]"}

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


def is_ascii_letter(ch: str) -> bool:
    return ch.isascii() and ch.isalpha()


def is_compatibility_hangul_jamo(ch: str) -> bool:
    return "\u3130" <= ch <= "\u318f"
