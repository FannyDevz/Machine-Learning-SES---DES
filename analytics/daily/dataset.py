import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

def load_daily_data(kode_kota, tipe, start, end):
    engine = get_engine(DB_NAME)

    query = text("""
        SELECT
            tanggal,
            harga
        FROM history_data_beras
        WHERE kode_kota = :kode_kota
          AND tipe = :tipe
          AND tanggal BETWEEN :start AND :end
        ORDER BY tanggal
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "kode_kota": kode_kota,
                "tipe": tipe,
                "start": start,
                "end": end
            }
        )

    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df.set_index("tanggal", inplace=True)

    return df
