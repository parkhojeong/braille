from dataclasses import dataclass


@dataclass(frozen=True)
class Syllable:
    l: str
    v: str
    t: str
