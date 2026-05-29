from hangul.tokenizer import tokenize_print
from hangul.text import Text
from hangul.rules.latin_phrase import latin_number_phrase_span, latin_phrase_span


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
    assert tokens[0].is_hangul
    assert not tokens[0].is_latin
    assert tokens[2].is_space
    assert tokens[-1].is_punctuation


def test_tokenize_print_groups_numbers_and_symbols():
    tokens = tokenize_print("A4 + ㎡")

    assert [(token.kind, token.text, token.group_id) for token in tokens] == [
        ("LATIN_RUN", "A", 0),
        ("NUMBER", "4", 0),
        ("SPACE", " ", None),
        ("SYMBOL", "+", 1),
        ("SPACE", " ", None),
        ("SYMBOL", "㎡", 2),
    ]
    assert tokens[0].is_latin
    assert tokens[1].is_number
    assert tokens[3].is_symbol


def test_text_keeps_tokens_and_spans_separate():
    text = Text.from_print(
        "MP3 플레이어",
        span_scanners=(latin_number_phrase_span, latin_phrase_span),
    )

    assert text.raw == "MP3 플레이어"
    assert [(token.kind, token.text) for token in text.tokens[:3]] == [
        ("LATIN_RUN", "MP"),
        ("NUMBER", "3"),
        ("SPACE", " "),
    ]

    span = text.spans[0]
    assert (span.kind, span.start, span.end, span.rule_id) == (
        "LATIN_NUMBER_PHRASE",
        0,
        2,
        "rule-35",
    )
    assert span.starts_at(0)
    assert span.contains(1)
    assert not span.contains(2)
    assert [token.text for token in text.tokens_for(span)] == ["MP", "3"]
    assert text.text_for(span) == "MP3"
    assert text.span_starting_at(0) == span
    assert text.spans_containing(1) == (span,)
    assert text.previous_token(1) == text.tokens[0]
    assert text.next_token(1) == text.tokens[2]
