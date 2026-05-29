from .jamo_encoder import encode_t, encode_v
from .jamo_basic_rules import rule_2_try_encode_l_ㄲㄸㅃㅆㅉ
from .tables import (
    FULL_SIGN_DOT,
    L_DOTS,
    RULE_10_ATTACHED_T_SIGN_DOT,
)


def rule_3_to_5_try_encode_t_role(ch: str, role: str) -> list[str] | None:
    """자모가 받침 역할이면 제3~5항의 받침 규칙으로 적는다."""
    if role == "t":
        return encode_t(ch)
    return None


def rule_8_or_9_try_encode_standalone_jamo(ch: str, role: str) -> list[str] | None:
    """제8항 자음자나 모음자가 단독으로 쓰일 때에는 해당 글자 앞에 온표 =을 적어 나타내며, 자음자는 받침으로 적는다.

    제9항 한글의 자음자가 번호로 쓰일 때에는 온표를 앞세워 받침으로 적는다.
    """
    if role != "standalone":
        return None

    if ch in L_DOTS or rule_2_try_encode_l_ㄲㄸㅃㅆㅉ(ch) is not None:
        return [FULL_SIGN_DOT, *encode_t(ch)]
    return [FULL_SIGN_DOT, *encode_v(ch)]


def rule_10_try_encode_attached_t(ch: str, role: str) -> list[str] | None:
    """제10항 단독으로 쓰인 자음자가 단어에 붙어 나올 때에는 _을 앞세워 받침으로 적는다."""
    if role != "attached_t":
        return None

    return [RULE_10_ATTACHED_T_SIGN_DOT, *encode_t(ch)]
