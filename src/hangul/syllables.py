from dataclasses import dataclass


@dataclass(frozen=True)
class Syllable:
    l: str
    v: str
    t: str

    def parts(self) -> tuple[str, str, str]:
        return self.l, self.v, self.t

    def matches(self, l: str, v: str, t: str) -> bool:
        return self.parts() == (l, v, t)

    @property
    def has_final(self) -> bool:
        return self.t != ""
