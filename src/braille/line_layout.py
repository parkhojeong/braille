from collections.abc import Sequence
from dataclasses import dataclass

from .ascii import dots_to_ascii
from .cells import BrailleCells


@dataclass(frozen=True)
class BrailleLine:
    cells: BrailleCells

    @classmethod
    def from_dot_strings(cls, dots: Sequence[str]) -> "BrailleLine":
        return cls(BrailleCells.from_dot_strings(dots))

    @property
    def dot_strings(self) -> list[str]:
        return self.cells.dot_strings

    @property
    def ascii(self) -> str:
        return dots_to_ascii(self.cells)

    def padded(self, width: int) -> "BrailleLine":
        if len(self.cells) >= width:
            return self
        return BrailleLine.from_dot_strings(
            [*self.dot_strings, *([""] * (width - len(self.cells)))]
        )


@dataclass(frozen=True)
class BrailleLines:
    lines: tuple[BrailleLine, ...]

    @property
    def dot_lines(self) -> list[list[str]]:
        return [line.dot_strings for line in self.lines]

    @property
    def ascii_lines(self) -> list[str]:
        return [line.ascii for line in self.lines]

    @property
    def ascii(self) -> str:
        return "\n".join(self.ascii_lines)


def layout_braille_lines(
    cells: Sequence[str] | BrailleCells,
    *,
    width: int,
    pad: bool = False,
) -> BrailleLines:
    if isinstance(cells, BrailleCells):
        dots = cells.dot_strings
    else:
        dots = list(cells)

    lines: list[BrailleLine] = []
    for start in range(0, len(dots), width):
        line = BrailleLine.from_dot_strings(dots[start : start + width])
        if pad:
            line = line.padded(width)
        lines.append(line)

    if not lines:
        lines.append(BrailleLine.from_dot_strings([]).padded(width if pad else 0))

    return BrailleLines(tuple(lines))
