from braille import (
    BrailleCell,
    BrailleCells,
    ascii_to_cells,
    ascii_to_dots,
    dots_to_ascii,
    dots_to_unicode,
    layout_braille_lines,
    unicode_to_cells,
    unicode_to_dots,
)


def test_ascii_to_cells_keeps_braille_cell_meaning():
    cells = ascii_to_cells("ab")

    assert cells == BrailleCells(
        (
            BrailleCell.from_dot_string("1"),
            BrailleCell.from_dot_string("12"),
        )
    )
    assert cells.cells[0].dots == ("1",)
    assert cells.cells[1].dot_string == "12"
    assert cells.dot_strings == ["1", "12"]
    assert dots_to_ascii(cells) == "ab"


def test_ascii_to_dots_keeps_list_compatibility():
    assert ascii_to_dots("ab") == ["1", "12"]


def test_braille_cell_rejects_unsupported_dot_value():
    try:
        BrailleCell.from_dot_string("17")
    except ValueError as exc:
        assert "unsupported 6-dot braille dot" in str(exc)
    else:
        raise AssertionError("expected invalid dot value to fail")


def test_unicode_conversions_accept_braille_cells():
    cells = unicode_to_cells("⠁⠃")

    assert cells == BrailleCells(
        (
            BrailleCell.from_dot_string("1"),
            BrailleCell.from_dot_string("12"),
        )
    )
    assert cells.dot_strings == ["1", "12"]
    assert unicode_to_dots("⠁⠃") == ["1", "12"]
    assert dots_to_unicode(cells) == "⠁⠃"


def test_layout_braille_lines_keeps_line_boundaries_out_of_cells():
    lines = layout_braille_lines(ascii_to_dots("abcdef"), width=3)

    assert lines.dot_lines == [["1", "12", "14"], ["145", "15", "124"]]
    assert lines.ascii_lines == ["abc", "def"]
    assert lines.ascii == "abc\ndef"


def test_layout_braille_lines_can_pad_lines():
    lines = layout_braille_lines(ascii_to_dots("abcd"), width=3, pad=True)

    assert lines.ascii_lines == ["abc", "d``"]
