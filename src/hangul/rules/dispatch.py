from collections.abc import Callable, Sequence
from typing import TypeVar

RuleResultT = TypeVar("RuleResultT")
Rule = Callable[..., RuleResultT | None]


def try_encode_rules(
    rules: Sequence[Rule[RuleResultT]],
    *args: object,
) -> RuleResultT | None:
    for rule in rules:
        result = rule(*args)
        if result is not None:
            return result
    return None


def encode_dot(mapping: dict[str, str], key: str, label: str) -> list[str]:
    try:
        return [mapping[key]]
    except KeyError:
        raise NotImplementedError(f"unsupported {label}: {key}") from None
