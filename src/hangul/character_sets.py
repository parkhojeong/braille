PUNCTUATION = {"(", ")", ",", ".", "!", "?", "[", "]"}

SYMBOLS = {
    "#",
    "$",
    "%",
    "*",
    "+",
    "-",
    "/",
    ":",
    ";",
    "@",
    "^",
    "_",
    "~",
    "·",
    "―",
    "‘",
    "’",
    "“",
    "”",
    "…",
    "※",
    "○",
    "△",
    "□",
    "×",
    "←",
    "→",
    "↔",
    "㎡",
    "ː",
    "￦",
    "￡",
    "€",
    "°",
    "′",
    "″",
    "⅔",
    "①",
    "ⓐ",
    "㉮",
    "Å",
    "℃",
    "℉",
    "㎏",
    "㎜",
    "㎥",
    "Ω",
    "‰",
    "æ",
    "ə",
    "ŋ",
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


def is_ascii_letter(ch: str) -> bool:
    return ch.isascii() and ch.isalpha()


def is_ascii_digit(ch: str) -> bool:
    return ch.isascii() and ch.isdigit()


def is_greek_letter(ch: str) -> bool:
    return ("\u0370" <= ch <= "\u03ff") or ("\u1f00" <= ch <= "\u1fff")


def is_compatibility_hangul_jamo(ch: str) -> bool:
    return "\u3130" <= ch <= "\u318f"
