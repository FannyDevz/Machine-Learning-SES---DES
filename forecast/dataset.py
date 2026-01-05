import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME


def load_monthly_series(
    kode_kota: str,
    tipe: str
) -> pd.Series:
    engine = get_engine(DB_NAME)

    query = text("""
        SELECT
            tahun,
            bulan,
            harga_ratarata
        FROM history_data_beras_monthly
        WHERE kode_kota = :kode_kota
            AND tipe = :tipe
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

    return df["harga_ratarata"]
