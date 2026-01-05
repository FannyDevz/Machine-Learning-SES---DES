import os
import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME
from utils.date import today, year

OUTPUT_DIR = "outputs/csv"

def export_harian_to_csv(
    start_date: str,
    end_date: str,
    filename: str | None = None
):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not start_date:
        start_date = today()
    if not end_date:
        end_date = today()

    if filename is None:
        filename = f"harga_beras_harian_{start_date}_to_{end_date}.csv"

    filepath = os.path.join(OUTPUT_DIR, filename)

    engine = get_engine(DB_NAME)

    query = text("""
        SELECT
            kode_kota,
            nama_kota,
            tipe,
            harga,
            tanggal
        FROM history_data_beras
        WHERE tanggal BETWEEN :start AND :end
        ORDER BY kode_kota, tipe, tanggal
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "start": start_date,
                "end": end_date
            }
        )

    if df.empty:
        print("⚠️  Tidak ada data untuk rentang tanggal tersebut.")
        return

    df.to_csv(filepath, index=False)
    print(f"✅ Export selesai: {filepath}")
    print(f"   Total rows: {len(df)}")


def export_monthly_to_csv(
    tahun: int | None = None,
    filename: str | None = None
):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not tahun:
        tahun = year()
        
    if filename is None:
        filename = "harga_beras_monthly.csv" if tahun is None else f"harga_beras_monthly_{tahun}.csv"

    filepath = os.path.join(OUTPUT_DIR, filename)

    engine = get_engine(DB_NAME)

    query = """
        SELECT
            kode_kota,
            nama_kota,
            tipe,
            harga_ratarata,
            harga_tertinggi,
            harga_terendah,
            bulan,
            tahun,
            cnt_hari
        FROM history_data_beras_monthly
    """

    params = {}
    if tahun is not None:
        query += " WHERE tahun = :tahun"
        params["tahun"] = tahun

    query += " ORDER BY kode_kota, tipe, tahun, bulan"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    if df.empty:
        print("⚠️  Tidak ada data bulanan.")
        return

    df.to_csv(filepath, index=False)
    print(f"✅ Export bulanan selesai: {filepath}")
    print(f"   Total rows: {len(df)}")