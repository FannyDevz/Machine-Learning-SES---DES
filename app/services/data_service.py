import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

engine = get_engine(DB_NAME)

def get_daftar_kota():
    query = text("""
        SELECT DISTINCT kode_kota
        FROM history_data_komoditas
        ORDER BY kode_kota
    """)
    df = pd.read_sql(query, engine)
    return df["kode_kota"].tolist()


def get_daftar_komoditas():
    """Daftar (komoditas_id, komoditas_nama) yang tersedia di data harian."""
    query = text("""
        SELECT DISTINCT komoditas_id, komoditas_nama
        FROM history_data_komoditas
        ORDER BY komoditas_nama
    """)
    df = pd.read_sql(query, engine)
    return list(zip(df["komoditas_id"].astype(int), df["komoditas_nama"]))


def get_overview():
    """Ringkasan isi database untuk dashboard beranda."""
    query = text("""
        SELECT
            COUNT(*)                       AS total_baris,
            COUNT(DISTINCT kode_kota)      AS total_kota,
            COUNT(DISTINCT komoditas_id)   AS total_komoditas,
            MIN(tanggal)                   AS tgl_awal,
            MAX(tanggal)                   AS tgl_akhir
        FROM history_data_komoditas
    """)
    with engine.connect() as conn:
        row = conn.execute(query).mappings().first()
    return dict(row) if row else {}
