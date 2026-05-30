from braille.ascii import dots_to_ascii
from braille.line_layout import BrailleLines, layout_braille_lines

from .token_encoder import encode_inkprint_text_to_dots


def inkprint_to_braille_dots(
    text: str,
    *,
    jamo_role: str = "l",
    line_width: int | None = None,
    initial_line_position: int = 0,
) -> list[str]:
    return encode_inkprint_text_to_dots(
        text,
        jamo_role=jamo_role,
        line_width=line_width,
        initial_line_position=initial_line_position,
    )


def inkprint_to_braille_ascii(text: str) -> str:
    return dots_to_ascii(inkprint_to_braille_dots(text))


def inkprint_to_braille_lines(
    text: str,
    *,
    width: int,
    jamo_role: str = "l",
    pad: bool = False,
) -> BrailleLines:
    return layout_braille_lines(
        inkprint_to_braille_dots(text, jamo_role=jamo_role, line_width=width),
        width=width,
        pad=pad,
    )
