import pandas as pd
import numpy as np


# =========================
# Fungsi yang akan dites
# =========================
def fill_harga(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["harga"] = df["harga"].fillna(
        df.groupby(
            ["kode_kota", "tipe", "tanggal"]
        )["harga"].transform("mean")
    )
    df.dropna(subset=["harga"], inplace=True)

    return df


# =========================
# Test runner
# =========================
def run_tests():
    print("=" * 60)
    print("TEST fill_harga")
    print("=" * 60)

    # Data contoh
    data = [
        # kota A, tipe 1, tanggal sama
        {"kode_kota": "A", "tipe": "1", "tanggal": "2025-01-01", "harga": 10000},
        {"kode_kota": "A", "tipe": "1", "tanggal": "2025-01-01", "harga": np.nan},
        {"kode_kota": "A", "tipe": "1", "tanggal": "2025-01-01", "harga": 20000},

        # kota B, semua NaN → harus terhapus
        {"kode_kota": "B", "tipe": "1", "tanggal": "2025-01-01", "harga": np.nan},
        {"kode_kota": "B", "tipe": "1", "tanggal": "2025-01-01", "harga": np.nan},
    ]

    df_before = pd.DataFrame(data)
    df_after = fill_harga(df_before)

    print("Before rows:", len(df_before))
    print("After rows :", len(df_after))
    print("-" * 60)

    # Tampilkan perubahan per baris
    for i, row in df_after.iterrows():
        print(
            f"row {i} -> kota: {row['kode_kota']} | tipe: {row['tipe']} | "
            f"tanggal: {row['tanggal']} | harga: {row['harga']}"
        )

    # Validasi sederhana
    # Harga rata-rata kota A = (10000 + 20000) / 2 = 15000
    expected_value = 15000
    filled_value = df_after.iloc[1]["harga"]

    status = "PASS" if filled_value == expected_value else "FAIL"
    print("-" * 60)
    print(
        f"before: NaN | after: {filled_value} | expect: {expected_value} | result: {status}"
    )


# =========================
# Entry point
# =========================
if __name__ == "__main__":
    run_tests()
