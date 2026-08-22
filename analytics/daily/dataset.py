import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

def load_daily_data(kode_kota, komoditas_id, start, end):
    engine = get_engine(DB_NAME)

    query = text("""
        SELECT
            tanggal,
            harga
        FROM history_data_komoditas
        WHERE kode_kota = :kode_kota
          AND komoditas_id = :komoditas_id
          AND tanggal BETWEEN :start AND :end
        ORDER BY tanggal
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "kode_kota": kode_kota,
                "komoditas_id": komoditas_id,
                "start": start,
                "end": end
            }
        )

    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df.set_index("tanggal", inplace=True)

    return df
