from braille.ascii import ascii_to_dots

from .context import RuleContext, RuleResult


def is_latin_text(ctx: RuleContext) -> bool:
    return all(token.kind in {"LATIN_RUN", "SPACE"} for token in ctx.tokens)


def encode_latin_run(text: str, *, indicators: bool = True) -> list[str]:
    cells: list[str] = ascii_to_dots("0") if indicators else []
    index = 0

    if text and text[0].isupper():
        cells.extend(ascii_to_dots(","))

    lower_text = text.lower()
    while index < len(lower_text):
        if lower_text[index : index + 2] == "ar":
            cells.extend(ascii_to_dots(">"))
            index += 2
            continue

        cells.extend(ascii_to_dots(lower_text[index]))
        index += 1

    if indicators:
        cells.extend(ascii_to_dots("4"))
    return cells


def encode_latin(ctx: RuleContext) -> RuleResult | None:
    if ctx.token.kind != "LATIN_RUN":
        return None

    return RuleResult(
        encode_latin_run(
            ctx.token.text,
            indicators=not is_latin_text(ctx),
        )
    )
