import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME


def get_harga_harian(
    start_date: str,
    end_date: str,
    tipe: str | None = None,
    kode_kota: str | None = None
) -> pd.DataFrame:

    query = """
        SELECT
            kode_kota,
            nama_kota,
            tipe,
            harga,
            tanggal
        FROM history_data_beras
        WHERE tanggal BETWEEN :start AND :end
    """

    params = {
        "start": start_date,
        "end": end_date
    }

    if tipe:
        query += " AND tipe = :tipe"
        params["tipe"] = tipe

    if kode_kota:
        query += " AND kode_kota = :kode_kota"
        params["kode_kota"] = kode_kota

    query += " ORDER BY tanggal ASC"

    engine = get_engine(DB_NAME)

    # ⬇️ INI KUNCI UTAMA
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    return df


def get_kode_kota_type() -> pd.DataFrame:
    query = text("""
        SELECT DISTINCT
            kode_kota,
            tipe
        FROM history_data_beras_monthly
        ORDER BY kode_kota, tipe
    """)

    engine = get_engine(DB_NAME)

  
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    return [(row[0], row[1]) for row in result]


def get_kode_kota() -> pd.DataFrame:
    query = text("""
        SELECT DISTINCT
            kode_kota
        FROM history_data_beras_monthly
        ORDER BY kode_kota
    """)

    engine = get_engine(DB_NAME)

  
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
    return result