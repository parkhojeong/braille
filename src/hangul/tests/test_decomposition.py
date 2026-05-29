from hangul import decompose_precomposed_hangul_syllable


CASES = {
    "가": ("ㄱ", "ㅏ", ""),
    "거": ("ㄱ", "ㅓ", ""),
    "값": ("ㄱ", "ㅏ", "ㅄ"),
    "꽃": ("ㄲ", "ㅗ", "ㅊ"),
    "힣": ("ㅎ", "ㅣ", "ㅎ"),
    "A": None,
}


def test_decompose_precomposed_hangul_syllable():
    for ch, expected in CASES.items():
        assert decompose_precomposed_hangul_syllable(ch) == expected


def main() -> int:
    failures = []

    for ch, expected in CASES.items():
        actual = decompose_precomposed_hangul_syllable(ch)
        if actual != expected:
            failures.append((ch, expected, actual))

    for ch, expected, actual in failures:
        print(f"FAIL {ch}")
        print(f"  expected: {expected}")
        print(f"  actual:   {actual}")

    passed = len(CASES) - len(failures)
    print(f"hangul decomposition: {passed}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
