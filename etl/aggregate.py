from sqlalchemy import text
from database.connection import get_engine
from utils.logger import logger
from config.settings import DB_NAME


def aggregate_monthly(start_year: int | None = None, end_year: int | None = None):
    """
    Agregasi data harian menjadi bulanan.
    Bisa difilter tahun (opsional).
    """

    logger.info("Transformasi bulanan dimulai")
    engine = get_engine(DB_NAME)

    where_clause = ""
    params = {}

    if start_year and end_year:
        where_clause = "WHERE YEAR(tanggal) BETWEEN :start_year AND :end_year"
        params = {
            "start_year": start_year,
            "end_year": end_year
        }
        logger.info(f"Agregasi bulanan dimulai | tahun={start_year}-{end_year}")
        
    query = text(f"""
        INSERT INTO history_data_beras_monthly (
            kode_kota,
            nama_kota,
            tipe,
            harga_ratarata,
            harga_tertinggi,
            harga_terendah,
            bulan,
            tahun,
            cnt_hari
        )
        SELECT
            kode_kota,
            MAX(nama_kota) AS nama_kota,
            tipe,
            ROUND(AVG(harga)) AS harga_ratarata,
            MAX(harga) AS harga_tertinggi,
            MIN(harga) AS harga_terendah,
            MONTH(tanggal) AS bulan,
            YEAR(tanggal) AS tahun,
            COUNT(*) AS cnt_hari
        FROM history_data_beras
        {where_clause}
        GROUP BY
            kode_kota,
            tipe,
            YEAR(tanggal),
            MONTH(tanggal)
        ON DUPLICATE KEY UPDATE
            harga_ratarata = VALUES(harga_ratarata),
            harga_tertinggi = VALUES(harga_tertinggi),
            harga_terendah = VALUES(harga_terendah),
            cnt_hari = VALUES(cnt_hari),
            nama_kota = VALUES(nama_kota),
            updated_at = CURRENT_TIMESTAMP
    """)

    with engine.begin() as conn:
        conn.execute(query, params)
        
    logger.info("Transformasi bulanan selesai")
