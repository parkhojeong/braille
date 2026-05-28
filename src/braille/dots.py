DOT_VALUES = {
    "1": 0x01,
    "2": 0x02,
    "3": 0x04,
    "4": 0x08,
    "5": 0x10,
    "6": 0x20,
}


def validate_dot_cell(cell: str) -> None:
    for dot in cell:
        if dot not in DOT_VALUES:
            raise ValueError(f"unsupported 6-dot braille dot: {dot}")


def dot_cell_to_bitmask(cell: str) -> int:
    validate_dot_cell(cell)
    bitmask = 0
    for dot in cell:
        bitmask |= DOT_VALUES[dot]
    return bitmask
