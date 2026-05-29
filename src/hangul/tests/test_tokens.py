from hangul.tokenizer import tokenize_print


def test_tokenize_print_groups_hangul_latin_space_and_punctuation():
    tokens = tokenize_print("나는 Apple을 본다.")

    assert [(token.kind, token.text, token.group_id) for token in tokens] == [
        ("HANGUL_SYLLABLE", "나", 0),
        ("HANGUL_SYLLABLE", "는", 0),
        ("SPACE", " ", None),
        ("LATIN_RUN", "Apple", 1),
        ("HANGUL_SYLLABLE", "을", 1),
        ("SPACE", " ", None),
        ("HANGUL_SYLLABLE", "본", 2),
        ("HANGUL_SYLLABLE", "다", 2),
        ("PUNCTUATION", ".", 2),
    ]

    assert tokens[0].l == "ㄴ"
    assert tokens[0].v == "ㅏ"
    assert tokens[0].t == ""
