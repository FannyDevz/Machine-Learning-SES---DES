import pandas as pd
import numpy as np
import re
from utils.logger import logger

def _clean_harga(val):
    """
    Bersihkan harga:
    - 'Rp 15.000' -> 15000
    - '15.000' -> 15000
    - None / '' -> NaN
    """
    if pd.isna(val):
        return np.nan

    if isinstance(val, (int, float)):
        return val

    val = str(val).strip()

    if val == "":
        return np.nan

    # Ambil angka saja
    angka = re.sub(r"[^\d]", "", val)

    return int(angka) if angka else np.nan


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transform mulai | rows awal={len(df)}")
    before = len(df)
    
    df = df.copy()
    
    # 1️⃣ Bersihkan harga
    df["harga"] = df["harga"].apply(_clean_harga)

    # 2️⃣ Isi harga kosong dengan rata-rata harian per kota & tipe
    df["harga"] = df["harga"].fillna(
        df.groupby(
            ["kode_kota", "tipe", "tanggal"]
        )["harga"].transform("mean")
    )

    # 3️⃣ Drop yang masih kosong (kalau 1 grup full NaN)
    df.dropna(subset=["harga"], inplace=True)

    # 4️⃣ Pastikan integer & valid
    df["harga"] = df["harga"].astype(int)
    df = df[df["harga"] > 0]

    after = len(df)
    logger.info(
        f"Transform selesai | rows akhir={after} | drop={before - after}"
    )
    return df
