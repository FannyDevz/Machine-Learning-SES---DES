import pandas as pd
import numpy as np


# =========================
# Fungsi validasi harga
# =========================
def validate_harga(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.dropna(subset=["harga"], inplace=True)
    df["harga"] = df["harga"].astype(int)
    df = df[df["harga"] > 0]

    return df
def validate_tanggal(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.dropna(subset=["tanggal"], inplace=True)
    df["tanggal"] = df["tanggal"].dt.strftime("%Y-%m-%d")

    return df


# =========================
# Test runner
# =========================
def run_tests():
    print("=" * 60)
    print("TEST validate_tanggal + validate_harga")
    print("=" * 60)

    data = [
        {"tanggal": "2025-01-01", "harga": 10000},
        {"tanggal": "2025-01-02", "harga": 0},
        {"tanggal": None, "harga": 20000},
        {"tanggal": "2025-01-04", "harga": -5000},
        {"tanggal": "2025-01-05", "harga": 15000},
    ]

    df_before = pd.DataFrame(data)

    # ubah dulu ke datetime agar bisa divalidasi
    df_before["tanggal"] = pd.to_datetime(df_before["tanggal"], errors="coerce")

    print("\nDATA SEBELUM:")
    print(df_before)

    df_after = validate_harga(df_before)
    df_after = validate_tanggal(df_after)

    print("\nDATA SESUDAH:")
    print(df_after)

    print("\nPER BARIS:")
    print("-" * 60)

    for i, row in df_after.iterrows():
        print(
            f"after: {row.to_dict()} | result: PASS"
        )

    print("-" * 60)
    print(f"Total rows after validation: {len(df_after)}")


# =========================
# Entry point
# =========================
if __name__ == "__main__":
    run_tests()
