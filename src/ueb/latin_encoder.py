from .latin_tables import (
    UEB_CONTRACTION_ASCII,
    UEB_SINGLE_LETTER_WORD_INDICATOR_LETTERS,
    UEB_SHORTFORM_WORD_ASCII,
)


def encode_latin_lower_ascii(text: str, *, contractions: bool = True) -> str:
    parts: list[str] = []
    lower_text = text.lower()
    index = 0
    while index < len(lower_text):
        if contractions:
            for text_part, ascii_part in sorted(
                UEB_CONTRACTION_ASCII.items(),
                key=lambda item: len(item[0]),
                reverse=True,
            ):
                if lower_text.startswith(text_part, index):
                    parts.append(ascii_part)
                    index += len(text_part)
                    break
            else:
                parts.append(lower_text[index])
                index += 1
        else:
            parts.append(lower_text[index])
            index += 1

    return "".join(parts)


def encode_latin_run_ascii(text: str) -> str:
    parts: list[str] = []

    index = 0
    while index < len(text):
        if text[index].isupper():
            end = index + 1
            while end < len(text) and text[end].isupper():
                end += 1

            if end - index == 1:
                while end < len(text) and not text[end].isupper():
                    end += 1

            indicator = ",," if text[index:end].isupper() and end - index > 1 else ","
            run = text[index:end]
            encoded = encode_latin_lower_ascii(
                run,
                contractions=not (run.isupper() and len(run) > 1),
            )
            parts.append(f"{indicator}{encoded}")
            index = end
        else:
            end = index + 1
            while end < len(text) and not text[end].isupper():
                end += 1

            parts.append(encode_latin_lower_ascii(text[index:end]))
            index = end

    return "".join(parts)


def encode_latin_phrase_run_ascii(text: str) -> str:
    prefix = ""
    shortform = UEB_SHORTFORM_WORD_ASCII.get(text.lower())
    if shortform is not None:
        if text.isupper() and len(text) > 1:
            prefix = ",,"
        elif text[0].isupper():
            prefix = ","
        return f"{prefix}{shortform}"

    if len(text) == 1 and text.lower() in UEB_SINGLE_LETTER_WORD_INDICATOR_LETTERS:
        prefix = ";"
    return f"{prefix}{encode_latin_run_ascii(text)}"


def encode_capital_passage_ascii(words: list[str]) -> str:
    return f",,,{'`'.join(encode_latin_lower_ascii(word) for word in words)},'"
