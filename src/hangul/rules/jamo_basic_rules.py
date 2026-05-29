from .dispatch import encode_dot
from .jamo_tables import (
    RULE_4_T_DOTS,
    RULE_5_T_CLUSTER_DOTS,
    RULE_7_V_DOTS,
    TENSE_L_BASE,
)
from .tables import L_DOTS, T_DOTS, V_DOTS


def encode_tense_l(ch: str, base_dots: dict[str, str]) -> list[str] | None:
    base = TENSE_L_BASE.get(ch)
    if base is None:
        return None
    return ["6", base_dots[base]]


def rule_1_encode_l(l: str) -> list[str]:
    """제1항 기본 자음자 14개가 첫소리로 쓰일 때에는 다음과 같이 적는다."""
    return encode_dot(L_DOTS, l, "l")


def rule_1_try_encode_l_ㅇ(l: str) -> list[str] | None:
    """[다만1] ‘ㅇ’이 첫소리로 쓰일 때에는 점자로 이를 표기하지 않는다."""
    if l == "ㅇ":
        return []
    return None


def rule_2_try_encode_l_ㄲㄸㅃㅆㅉ(l: str) -> list[str] | None:
    """제2항 된소리 글자 ‘ㄲ, ㄸ, ㅃ, ㅆ, ㅉ’이 첫소리로 쓰일 때에는 ‘ㄱ, ㄷ, ㅂ, ㅅ, ㅈ’ 앞에 된소리표 ,을 적어 나타낸다."""
    return encode_tense_l(l, L_DOTS)


def rule_3_encode_t(t: str) -> list[str]:
    """제3항 기본 자음자 14개가 받침으로 쓰일 때에는 다음과 같이 적는다."""
    return encode_dot(T_DOTS, t, "t")


def rule_4_try_encode_t_ㄲㅆ(t: str) -> list[str] | None:
    """제4항 쌍받침 ‘ㄲ’은 aa으로 적고, 쌍받침 ‘ㅆ’은 약자인 /으로 적는다."""
    dots = RULE_4_T_DOTS.get(t)
    if dots is not None:
        return [*dots]
    return None


def rule_5_try_encode_t_cluster(t: str) -> list[str] | None:
    """제5항 겹받침은 각 받침 글자를 어울러 다음과 같이 적는다."""
    dots = RULE_5_T_CLUSTER_DOTS.get(t)
    if dots is not None:
        return [*dots]
    return None


def rule_6_encode_v(v: str) -> list[str]:
    """제6항 기본 모음자 10개는 다음과 같이 적는다."""
    return encode_dot(V_DOTS, v, "v")


def rule_7_try_encode_v_cluster(v: str) -> list[str] | None:
    """제7항 그 밖의 모음자 11개는 다음과 같이 적는다."""
    dots = RULE_7_V_DOTS.get(v)
    if dots is not None:
        return [*dots]
    return None
