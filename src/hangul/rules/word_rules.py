from collections.abc import Callable

from braille.ascii import ascii_to_dots

from .context import RuleContext, RuleResult
from .dispatch import try_encode_rules
from .encoder import encode_syllable
from .word_spacing_tables import BRAILLE_SPACING_TERMS

WordRule = Callable[[RuleContext], RuleResult | None]

WORD_ABBREVIATION_DOTS = {
    "그래서": ascii_to_dots("as"),
    "그러나": ascii_to_dots("ac"),
    "그러면": ascii_to_dots("a3"),
    "그러므로": ascii_to_dots("a5"),
    "그런데": ascii_to_dots("an"),
    "그리고": ascii_to_dots("au"),
    "그리하여": ascii_to_dots("a:"),
}

def encode_hangul_segment(ctx: RuleContext, start: int, end: int) -> list[str]:
    dots: list[str] = []
    for index in range(start, end):
        segment_ctx = RuleContext(ctx.tokens, index)
        dots.extend(encode_syllable(segment_ctx))
    return dots


def rule_braille_spacing_term(ctx: RuleContext) -> RuleResult | None:
    for term, segments in sorted(
        BRAILLE_SPACING_TERMS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if ctx.text_from_current(len(term)) != term:
            continue

        dots: list[str] = []
        offset = 0
        for segment_index, segment in enumerate(segments):
            if segment_index > 0:
                dots.append("")
            dots.extend(
                encode_hangul_segment(
                    ctx,
                    ctx.index + offset,
                    ctx.index + offset + len(segment),
                )
            )
            offset += len(segment)
        return RuleResult(dots, len(term))

    return None


def rule_18_try_encode_약어(ctx: RuleContext) -> RuleResult | None:
    """제18항 다음 단어들은 약어를 사용하여 적는다.

    [붙임] 약어 뒤에 다른 글자가 붙어 나올 때에도 약어를 사용하여 적는다.
    [다만] 약어 앞에 다른 글자가 붙어 나올 때에는 약어를 사용하지 않는다.
    """
    prefix_dots: list[str] = []
    if not ctx.is_group_start:
        if ctx.previous_group_text != "왜":
            return None
        prefix_dots = [""]

    for word, dots in sorted(
        WORD_ABBREVIATION_DOTS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if ctx.text_from_current(len(word)) == word:
            return RuleResult([*prefix_dots, *dots], len(word))

    return None


WORD_RULES: list[WordRule] = [
    rule_braille_spacing_term,
    rule_18_try_encode_약어,
]


def encode_word(ctx: RuleContext) -> RuleResult | None:
    return try_encode_rules(WORD_RULES, ctx)
