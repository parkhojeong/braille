from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Literal

DotValue = Literal["1", "2", "3", "4", "5", "6"]
DOT_VALUES = {"1", "2", "3", "4", "5", "6"}


@dataclass(frozen=True)
class BrailleCell:
    dots: tuple[DotValue, ...]

    @classmethod
    def from_dot_string(cls, dots: str) -> "BrailleCell":
        unsupported_dots = set(dots) - DOT_VALUES
        if unsupported_dots:
            raise ValueError(f"unsupported 6-dot braille dot: {unsupported_dots.pop()}")

        return cls(tuple(dots))  # type: ignore[arg-type]

    @property
    def dot_string(self) -> str:
        return "".join(self.dots)


@dataclass(frozen=True)
class BrailleCells:
    cells: tuple[BrailleCell, ...]

    @classmethod
    def from_dot_strings(cls, dots: Iterable[str]) -> "BrailleCells":
        return cls(tuple(BrailleCell.from_dot_string(dot) for dot in dots))

    @property
    def dot_strings(self) -> list[str]:
        return [cell.dot_string for cell in self.cells]

    def __iter__(self) -> Iterator[BrailleCell]:
        return iter(self.cells)

    def __len__(self) -> int:
        return len(self.cells)
