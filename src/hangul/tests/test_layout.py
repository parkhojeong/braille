from hangul import inkprint_to_braille_ascii, inkprint_to_braille_lines


def test_inkprint_to_braille_lines_wraps_logical_braille_cells():
    text = "가나다라마"

    lines = inkprint_to_braille_lines(text, width=3)

    assert lines.ascii == "$ci\n\"<e"
    assert lines.ascii.replace("\n", "") == inkprint_to_braille_ascii(text)


def test_inkprint_to_braille_lines_can_pad_output_lines():
    lines = inkprint_to_braille_lines("가나", width=3, pad=True)

    assert lines.ascii_lines == ["$c`"]
