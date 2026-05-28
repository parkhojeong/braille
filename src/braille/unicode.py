from .dots import DOT_VALUES, dot_cell_to_bitmask

BRAILLE_PATTERN_BASE = 0x2800
BRAILLE_PATTERN_END = 0x283F


def unicode_char_to_dots(ch: str) -> str:
    code_point = ord(ch)
    if not BRAILLE_PATTERN_BASE <= code_point <= BRAILLE_PATTERN_END:
        raise ValueError(f"not a Unicode braille pattern: {ch}")

    bitmask = code_point - BRAILLE_PATTERN_BASE
    dots = []
    for dot, value in DOT_VALUES.items():
        if bitmask & value:
            dots.append(dot)
    return "".join(dots)


def unicode_to_dots(text: str) -> list[str]:
    return [unicode_char_to_dots(ch) for ch in text]


def dots_to_unicode(cells: list[str]) -> str:
    return "".join(
        chr(BRAILLE_PATTERN_BASE + dot_cell_to_bitmask(cell))
        for cell in cells
    )
