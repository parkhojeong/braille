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

COMPOSITE_JUNGSEONG_DOTS = {
    "ㅐ": ["1235"],
    "ㅒ": [JUNGSEONG_DOTS["ㅑ"], "1235"],
    "ㅔ": ["1345"],
    "ㅖ": ["34"],
    "ㅘ": ["1236"],
    "ㅙ": ["1236", "1235"],
    "ㅚ": ["13456"],
    "ㅝ": ["1234"],
    "ㅞ": ["1234", "1235"],
    "ㅟ": [JUNGSEONG_DOTS["ㅜ"], "1235"],
    "ㅢ": ["2456"],
}

ABBREVIATED_A_DOTS = {
    "ㄱ": "1246",
    "ㄴ": CHOSEONG_DOTS["ㄴ"],
    "ㄷ": CHOSEONG_DOTS["ㄷ"],
    "ㅁ": CHOSEONG_DOTS["ㅁ"],
    "ㅂ": CHOSEONG_DOTS["ㅂ"],
    "ㅅ": "123",
    "ㅈ": CHOSEONG_DOTS["ㅈ"],
    "ㅋ": CHOSEONG_DOTS["ㅋ"],
    "ㅌ": CHOSEONG_DOTS["ㅌ"],
    "ㅍ": CHOSEONG_DOTS["ㅍ"],
    "ㅎ": CHOSEONG_DOTS["ㅎ"],
}

TENSE_ABBREVIATED_A_DOTS = {
    "ㄲ": ["6", ABBREVIATED_A_DOTS["ㄱ"]],
    "ㄸ": ["6", ABBREVIATED_A_DOTS["ㄷ"]],
    "ㅃ": ["6", ABBREVIATED_A_DOTS["ㅂ"]],
    "ㅆ": ["6", ABBREVIATED_A_DOTS["ㅅ"]],
    "ㅉ": ["6", ABBREVIATED_A_DOTS["ㅈ"]],
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
    "ㅆ": "34",
}

DOUBLE_JONGSEONG_DOTS = {
    "ㄲ": [JONGSEONG_DOTS["ㄱ"], JONGSEONG_DOTS["ㄱ"]],
    "ㅆ": [JONGSEONG_DOTS["ㅆ"]],
}

COMPOSITE_JONGSEONG_DOTS = {
    "ㄳ": [JONGSEONG_DOTS["ㄱ"], JONGSEONG_DOTS["ㅅ"]],
    "ㄵ": [JONGSEONG_DOTS["ㄴ"], JONGSEONG_DOTS["ㅈ"]],
    "ㄶ": [JONGSEONG_DOTS["ㄴ"], JONGSEONG_DOTS["ㅎ"]],
    "ㄺ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㄱ"]],
    "ㄻ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㅁ"]],
    "ㄼ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㅂ"]],
    "ㄽ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㅅ"]],
    "ㄾ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㅌ"]],
    "ㄿ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㅍ"]],
    "ㅀ": [JONGSEONG_DOTS["ㄹ"], JONGSEONG_DOTS["ㅎ"]],
    "ㅄ": [JONGSEONG_DOTS["ㅂ"], JONGSEONG_DOTS["ㅅ"]],
}

NEXT_IEUNG_CANCELS_ABBREVIATED_A = {
    "ㄴ",
    "ㄷ",
    "ㅁ",
    "ㅂ",
    "ㅈ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
}

VOWEL_JONGSEONG_ABBREVIATIONS = {
    ("ㅕ", "ㄹ"): "1256",
    ("ㅕ", "ㅇ"): "12456",
    ("ㅡ", "ㄴ"): "1356",
    ("ㅓ", "ㄴ"): "23456",
    ("ㅕ", "ㄴ"): "16",
    ("ㅗ", "ㅇ"): "123456",
}
