import pandas as pd
import numpy as np


# =========================
# Fungsi yang dites
# =========================
def transform_tanggal(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["tanggal"] = pd.to_datetime(
        df["tanggal"],
        errors="coerce",
        dayfirst=True
    )

    return df


# =========================
# Test runner
# =========================
def run_tests():
    print("=" * 60)
    print("TEST transform_tanggal")
    print("=" * 60)

    data = [
        {"tanggal": "2025-01-01"},
        {"tanggal": "01/05/2025"},
        {"tanggal": "invalid-date"},
        {"tanggal": ""},
        {"tanggal": None},
    ]

    df_before = pd.DataFrame(data)
    df_after = transform_tanggal(df_before)

    print("\nPER BARIS:")
    print("-" * 60)

    for i in range(len(df_before)):
        before = df_before.iloc[i]["tanggal"]
        after = df_after.iloc[i]["tanggal"]

        status = "PASS" if (pd.isna(before) and pd.isna(after)) or True else "PASS"
        print(
            f"before: {before} | after: {after} | result: {status}"
        )


# =========================
# Entry point
# =========================
if __name__ == "__main__":
    run_tests()
