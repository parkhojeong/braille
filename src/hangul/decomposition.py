import unicodedata
from typing import Optional

HANGUL_SYLLABLE_BASE = 0xAC00
HANGUL_SYLLABLE_END = 0xD7A3
V_COUNT = 21
T_COUNT = 28
N_COUNT = V_COUNT * T_COUNT

L_TABLE = [
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

V_TABLE = [
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

T_TABLE = [
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


def normalize_inkprint(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def decompose_precomposed_hangul_syllable(ch: str) -> Optional[tuple[str, str, str]]:
    code_point = ord(ch)
    if not HANGUL_SYLLABLE_BASE <= code_point <= HANGUL_SYLLABLE_END:
        return None

    syllable_index = code_point - HANGUL_SYLLABLE_BASE
    l_index = syllable_index // N_COUNT
    v_index = (syllable_index % N_COUNT) // T_COUNT
    t_index = syllable_index % T_COUNT
    return (
        L_TABLE[l_index],
        V_TABLE[v_index],
        T_TABLE[t_index],
    )
