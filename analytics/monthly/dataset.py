import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

def load_monthly_data(kode_kota, tipe, start_year=None, end_year=None):
    engine = get_engine(DB_NAME)

    query = """
        SELECT
            tahun,
            bulan,
            harga_ratarata,
            harga_tertinggi,
            harga_terendah,
            cnt_hari
        FROM history_data_beras_monthly
        WHERE kode_kota = :kode_kota
          AND tipe = :tipe
    """

    params = {
        "kode_kota": kode_kota,
        "tipe": tipe
    }

    if start_year:
        query += " AND tahun >= :start_year"
        params["start_year"] = start_year

    if end_year:
        query += " AND tahun <= :end_year"
        params["end_year"] = end_year

    query += " ORDER BY tahun, bulan"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    df["date"] = pd.to_datetime(
        df["tahun"].astype(str) + "-" + df["bulan"].astype(str) + "-01"
    )
    df.set_index("date", inplace=True)

    return df
