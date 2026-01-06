import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME


def load_monthly_series(
    kode_kota: str,
    tipe: str,
    jenis_data: str = "harga_ratarata"
) -> pd.Series:
    
    ALLOWED_COLS = {"harga_ratarata", "harga_tertinggi", "harga_terendah"}
        
    if jenis_data not in ALLOWED_COLS:
        raise ValueError("jenis_data tidak valid")
    
    engine = get_engine(DB_NAME)

    query = text("""
        SELECT
            tahun,
            bulan,
            """ + jenis_data + """
        FROM history_data_beras_monthly
        WHERE kode_kota = :kode_kota
            AND tipe = :tipe 
            AND (
            (tahun > 2022 OR (tahun = 2022 AND bulan >= 1)) -- Mulai Jan 2022
            AND 
            (tahun < 2025 OR (tahun = 2025 AND bulan <= 6)) -- Selesai Jun 2025
        )
        ORDER BY tahun, bulan
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "kode_kota": kode_kota,
                "tipe": tipe
            }
        )

    if df.empty:
        raise ValueError("Data kosong untuk kombinasi ini")

    df["date"] = pd.to_datetime(
        df["tahun"].astype(str) + "-" + df["bulan"].astype(str) + "-01"
    )

    df.set_index("date", inplace=True)

    return df["" + jenis_data + ""]


