CHOSEONG_DOTS = {
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
    "ㄲ": ["6", CHOSEONG_DOTS["ㄱ"]],
    "ㄸ": ["6", CHOSEONG_DOTS["ㄷ"]],
    "ㅃ": ["6", CHOSEONG_DOTS["ㅂ"]],
    "ㅆ": ["6", CHOSEONG_DOTS["ㅅ"]],
    "ㅉ": ["6", CHOSEONG_DOTS["ㅈ"]],
}

JUNGSEONG_DOTS = {
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

JONGSEONG_DOTS = {
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
    "ㄲ": "1-1",
    "ㅆ": "34",
    "ㄳ": "1-3",
    "ㄵ": "25-13",
    "ㄶ": "25-356",
    "ㄺ": "2-1",
    "ㄻ": "2-26",
    "ㄼ": "2-12",
    "ㄽ": "2-3",
    "ㄾ": "2-236",
    "ㄿ": "2-256",
    "ㅀ": "2-356",
    "ㅄ": "12-3",
}


def encode_choseong(choseong: str) -> list[str]:
    if choseong == "ㅇ":
        return []
    if choseong in TENSE_CHOSEONG_DOTS:
        return TENSE_CHOSEONG_DOTS[choseong]
    return [CHOSEONG_DOTS[choseong]]


def encode_jungseong(jungseong: str) -> list[str]:
    return [JUNGSEONG_DOTS[jungseong]]


def encode_jongseong(jongseong: str) -> list[str]:
    if not jongseong:
        return []
    return JONGSEONG_DOTS[jongseong].split("-")


def encode_syllable(choseong: str, jungseong: str, jongseong: str) -> list[str]:
    if jungseong == "ㅏ":
        if choseong == "ㅅ":
            return ["123", *encode_jongseong(jongseong)]
        if choseong in {"ㄷ", "ㅌ", "ㅎ"}:
            return [CHOSEONG_DOTS[choseong], *encode_jongseong(jongseong)]

    return [
        *encode_choseong(choseong),
        *encode_jungseong(jungseong),
        *encode_jongseong(jongseong),
    ]


def encode_standalone_jamo(ch: str, role: str) -> list[str]:
    if ch in TENSE_CHOSEONG_DOTS:
        return TENSE_CHOSEONG_DOTS[ch]

    if role == "jongseong" and ch in JONGSEONG_DOTS:
        return JONGSEONG_DOTS[ch].split("-")

    if ch in CHOSEONG_DOTS:
        return [CHOSEONG_DOTS[ch]]

    raise NotImplementedError(f"unsupported character: {ch}")
