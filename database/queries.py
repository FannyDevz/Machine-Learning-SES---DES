import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME


def get_harga_harian(
    start_date: str,
    end_date: str,
    komoditas_id: int | None = None,
    kode_kota: str | None = None
) -> pd.DataFrame:

    query = """
        SELECT
            kode_kota,
            nama_kota,
            komoditas_id,
            komoditas_nama,
            harga,
            tanggal
        FROM history_data_komoditas
        WHERE tanggal BETWEEN :start AND :end
    """

    params = {
        "start": start_date,
        "end": end_date
    }

    if komoditas_id:
        query += " AND komoditas_id = :komoditas_id"
        params["komoditas_id"] = komoditas_id

    if kode_kota:
        query += " AND kode_kota = :kode_kota"
        params["kode_kota"] = kode_kota

    query += " ORDER BY tanggal ASC"

    engine = get_engine(DB_NAME)

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    return df


def get_kode_kota_komoditas() -> list[tuple[str, int]]:
    """Daftar kombinasi (kode_kota, komoditas_id) yang punya data bulanan."""
    query = text("""
        SELECT DISTINCT
            kode_kota,
            komoditas_id
        FROM history_data_komoditas_monthly
        ORDER BY kode_kota, komoditas_id
    """)

    engine = get_engine(DB_NAME)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    return [(row[0], int(row[1])) for row in result]


def get_kode_kota() -> list:
    query = text("""
        SELECT DISTINCT
            kode_kota
        FROM history_data_komoditas_monthly
        ORDER BY kode_kota
    """)

    engine = get_engine(DB_NAME)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
    return [row[0] for row in result]
