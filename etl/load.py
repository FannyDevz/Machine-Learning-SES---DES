from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME
from utils.logger import logger

def load_to_db(df):
    """
    Upsert data ke history_data_beras:
    - Insert jika belum ada
    - Update harga jika berubah
    - Skip jika sama
    """
    if df.empty:
        logger.warning("Load dibatalkan | dataframe kosong")
        return

    engine = get_engine(DB_NAME)

    query = text("""
        INSERT INTO history_data_beras (
            kode_kota,
            nama_kota,
            tipe,
            harga,
            tanggal
        )
        VALUES (
            :kode_kota,
            :nama_kota,
            :tipe,
            :harga,
            :tanggal
        )
        ON DUPLICATE KEY UPDATE
            harga = IF(harga <> VALUES(harga), VALUES(harga), harga),
            nama_kota = VALUES(nama_kota)
    """)

    rows = df.to_dict(orient="records")

    with engine.begin() as conn:
        try:        
            conn.execute(query, rows)
            logger.info(
                f"Load sukses | rows={len(rows)}"
            )
        except Exception as e:
            logger.error(
                f"Load gagal | error={str(e)}"
            )
            raise
