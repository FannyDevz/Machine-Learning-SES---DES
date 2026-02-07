import numpy as np
import pandas as pd
import re


# =========================
# Fungsi yang akan dites
# =========================
def _clean_harga(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return val
    val = str(val).strip()
    if val == "":
        return np.nan
    angka = re.sub(r"[^\d]", "", val)
    return int(angka) if angka else np.nan


# =========================
# Test cases
# =========================
def run_tests():
    test_cases = [
        ("Integer", 1000, 1000),
        ("Float", 1000.5, 1000.5),
        ("String angka", "15000", 15000),
        ("Format Rp", "Rp 15.000", 15000),
        ("Format koma", "20,500", 20500),
        ("Empty string", "", np.nan),
        ("NaN", np.nan, np.nan),
        ("Non numeric", "abc", np.nan),
    ]

    print("=" * 50)
    print("TEST _clean_harga")
    print("=" * 50)

    passed = 0

    for name, before, expected in test_cases:
        result = _clean_harga(before)

        if pd.isna(expected):
            ok = pd.isna(result)
        else:
            ok = result == expected

        status = "PASS" if ok else "FAIL"

        print(f"{name}")
        print(f"before: {before} | after: {result} | expect: {expected} | result: {status}")
        print("-" * 50)

        if ok:
            passed += 1

    print(f"Summary: {passed}/{len(test_cases)} tests passed")


# =========================
# Entry point
# =========================
if __name__ == "__main__":
    run_tests()
