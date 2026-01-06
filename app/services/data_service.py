import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

engine = get_engine(DB_NAME)

def get_daftar_kota():
    query = text("""
        SELECT DISTINCT kode_kota
        FROM history_data_beras
        ORDER BY kode_kota
    """)
    df = pd.read_sql(query, engine)
    return df["kode_kota"].tolist()
