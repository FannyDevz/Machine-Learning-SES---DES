# analytics/compare.py
import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

def load_compare_data(kode_kota_list, tipe, start_date, end_date):
    engine = get_engine(DB_NAME)

    query = text("""
        SELECT
            kode_kota,
            tanggal,
            harga
        FROM history_data_beras
        WHERE kode_kota IN :kota
            AND tipe = :tipe
            AND tanggal BETWEEN :start AND :end
        ORDER BY tanggal
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "kota": tuple(kode_kota_list),
                "tipe": tipe,
                "start": start_date,
                "end": end_date
            }
        )

    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df
