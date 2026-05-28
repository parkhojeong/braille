import unicodedata
from typing import Optional

HANGUL_SYLLABLE_BASE = 0xAC00
HANGUL_SYLLABLE_END = 0xD7A3
JUNGSEONG_COUNT = 21
JONGSEONG_COUNT = 28
SYLLABLES_PER_CHOSEONG = JUNGSEONG_COUNT * JONGSEONG_COUNT

CHOSEONG = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

JUNGSEONG = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

JONGSEONG = [
    "",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]


def normalize_print(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def decompose_precomposed_hangul_syllable(ch: str) -> Optional[tuple[str, str, str]]:
    code_point = ord(ch)
    if not HANGUL_SYLLABLE_BASE <= code_point <= HANGUL_SYLLABLE_END:
        return None

    syllable_index = code_point - HANGUL_SYLLABLE_BASE
    choseong_index = syllable_index // SYLLABLES_PER_CHOSEONG
    jungseong_index = (syllable_index % SYLLABLES_PER_CHOSEONG) // JONGSEONG_COUNT
    jongseong_index = syllable_index % JONGSEONG_COUNT
    return (
        CHOSEONG[choseong_index],
        JUNGSEONG[jungseong_index],
        JONGSEONG[jongseong_index],
    )
