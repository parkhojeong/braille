from collections.abc import Sequence

from .cells import BrailleCells

ASCII_TO_DOTS = {
    " ": "",
    "!": "2346",
    '"': "5",
    "#": "3456",
    "$": "1246",
    "%": "146",
    "&": "12346",
    "'": "3",
    "(": "12356",
    ")": "23456",
    "*": "16",
    "+": "346",
    ",": "6",
    "-": "36",
    ".": "46",
    "/": "34",
    "0": "356",
    "1": "2",
    "2": "23",
    "3": "25",
    "4": "256",
    "5": "26",
    "6": "235",
    "7": "2356",
    "8": "236",
    "9": "35",
    ":": "156",
    ";": "56",
    "<": "126",
    "=": "123456",
    ">": "345",
    "?": "1456",
    "@": "4",
    "[": "246",
    "\\": "1256",
    "]": "12456",
    "^": "45",
    "_": "456",
    "`": "",
    "|": "1256",
    "}": "12456",
    "\n": "\n",
}

LETTER_TO_DOTS = {
    "A": "1",
    "B": "12",
    "C": "14",
    "D": "145",
    "E": "15",
    "F": "124",
    "G": "1245",
    "H": "125",
    "I": "24",
    "J": "245",
    "K": "13",
    "L": "123",
    "M": "134",
    "N": "1345",
    "O": "135",
    "P": "1234",
    "Q": "12345",
    "R": "1235",
    "S": "234",
    "T": "2345",
    "U": "136",
    "V": "1236",
    "W": "2456",
    "X": "1346",
    "Y": "13456",
    "Z": "1356",
}

ASCII_TO_DOTS.update(LETTER_TO_DOTS)
ASCII_TO_DOTS.update({ch.lower(): dots for ch, dots in LETTER_TO_DOTS.items()})

CANONICAL_ASCII_BY_DOTS = {
    "146": "%",
    "246": "[",
    "345": ">",
}


def _ascii_preference(ch: str) -> tuple[int, str]:
    if ch == "`":
        return (0, ch)
    if ch == " ":
        return (9, ch)
    if ch.islower():
        return (1, ch)
    if ch.isupper():
        return (2, ch)
    return (3, ch)


def _build_dots_to_ascii() -> dict[str, str]:
    candidates: dict[str, list[str]] = {}
    for ascii_ch, dots in ASCII_TO_DOTS.items():
        candidates.setdefault(dots, []).append(ascii_ch)
    result = {}
    for dots, chars in candidates.items():
        if dots in CANONICAL_ASCII_BY_DOTS:
            result[dots] = CANONICAL_ASCII_BY_DOTS[dots]
        else:
            result[dots] = sorted(chars, key=_ascii_preference)[0]
    return result


DOTS_TO_ASCII = _build_dots_to_ascii()


def ascii_to_cells(text: str) -> BrailleCells:
    return BrailleCells.from_dot_strings(ASCII_TO_DOTS[ch] for ch in text)


def ascii_to_dots(text: str) -> list[str]:
    return ascii_to_cells(text).dot_strings


def dots_to_ascii(cells: Sequence[str] | BrailleCells) -> str:
    if isinstance(cells, BrailleCells):
        cells = cells.dot_strings
    return "".join(DOTS_TO_ASCII[cell] for cell in cells)
