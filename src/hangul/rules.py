CHOSEONG_DOT = {
    "ㄱ": "4",
    "ㄴ": "14",
    "ㄷ": "24",
    "ㄹ": "5",
    "ㅁ": "15",
    "ㅂ": "45",
    "ㅅ": "6",
    "ㅇ": "1245",
    "ㅈ": "46",
    "ㅊ": "56",
    "ㅋ": "124",
    "ㅌ": "125",
    "ㅍ": "145",
    "ㅎ": "245",
}

TENSE_CHOSEONG_DOTS = {
    "ㄲ": ["6", CHOSEONG_DOT["ㄱ"]],
    "ㄸ": ["6", CHOSEONG_DOT["ㄷ"]],
    "ㅃ": ["6", CHOSEONG_DOT["ㅂ"]],
    "ㅆ": ["6", CHOSEONG_DOT["ㅅ"]],
    "ㅉ": ["6", CHOSEONG_DOT["ㅈ"]],
}

JUNGSEONG_DOT = {
    "ㅏ": "126",
    "ㅑ": "345",
    "ㅓ": "234",
    "ㅕ": "156",
    "ㅗ": "136",
    "ㅛ": "346",
    "ㅜ": "134",
    "ㅠ": "146",
    "ㅡ": "246",
    "ㅚ": "13456",
    "ㅣ": "135",
}

JONGSEONG_DOT = {
    "ㄱ": "1",
    "ㄴ": "25",
    "ㄷ": "35",
    "ㄹ": "2",
    "ㅁ": "26",
    "ㅂ": "12",
    "ㅅ": "3",
    "ㅇ": "2356",
    "ㅈ": "13",
    "ㅊ": "23",
    "ㅋ": "235",
    "ㅌ": "236",
    "ㅍ": "256",
    "ㅎ": "356",
    "ㅆ": "34",
}

COMPOSITE_JONGSEONG_DOTS = {
    "ㄲ": [JONGSEONG_DOT["ㄱ"], JONGSEONG_DOT["ㄱ"]],
    "ㄳ": [JONGSEONG_DOT["ㄱ"], JONGSEONG_DOT["ㅅ"]],
    "ㄵ": [JONGSEONG_DOT["ㄴ"], JONGSEONG_DOT["ㅈ"]],
    "ㄶ": [JONGSEONG_DOT["ㄴ"], JONGSEONG_DOT["ㅎ"]],
    "ㄺ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㄱ"]],
    "ㄻ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㅁ"]],
    "ㄼ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㅂ"]],
    "ㄽ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㅅ"]],
    "ㄾ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㅌ"]],
    "ㄿ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㅍ"]],
    "ㅀ": [JONGSEONG_DOT["ㄹ"], JONGSEONG_DOT["ㅎ"]],
    "ㅄ": [JONGSEONG_DOT["ㅂ"], JONGSEONG_DOT["ㅅ"]],
}


def encode_choseong(choseong: str) -> list[str]:
    if choseong == "ㅇ":
        return []
    if choseong in TENSE_CHOSEONG_DOTS:
        return TENSE_CHOSEONG_DOTS[choseong]
    return [CHOSEONG_DOT[choseong]]


def encode_jungseong(jungseong: str) -> list[str]:
    return [JUNGSEONG_DOT[jungseong]]


def encode_jongseong(jongseong: str) -> list[str]:
    if not jongseong:
        return []
    if jongseong in COMPOSITE_JONGSEONG_DOTS:
        return COMPOSITE_JONGSEONG_DOTS[jongseong]
    return [JONGSEONG_DOT[jongseong]]


def encode_syllable(choseong: str, jungseong: str, jongseong: str) -> list[str]:
    if jungseong == "ㅏ":
        if choseong == "ㅅ":
            return ["123", *encode_jongseong(jongseong)]
        if choseong in {"ㄷ", "ㅌ", "ㅎ"}:
            return [CHOSEONG_DOT[choseong], *encode_jongseong(jongseong)]

    return [
        *encode_choseong(choseong),
        *encode_jungseong(jungseong),
        *encode_jongseong(jongseong),
    ]


def encode_standalone_jamo(ch: str, role: str) -> list[str]:
    if ch in TENSE_CHOSEONG_DOTS:
        return TENSE_CHOSEONG_DOTS[ch]

    if role == "jongseong":
        return encode_jongseong(ch)

    if ch in CHOSEONG_DOT:
        return [CHOSEONG_DOT[ch]]

    raise NotImplementedError(f"unsupported character: {ch}")
