from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME
from utils.logger import logger

TABLES = [
    """
    CREATE TABLE IF NOT EXISTS history_data_komoditas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode_kota VARCHAR(50) NOT NULL,
        nama_kota VARCHAR(100) NOT NULL,
        komoditas_id INT NOT NULL,
        komoditas_nama VARCHAR(150) NOT NULL,
        harga INT NOT NULL,
        tanggal DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_harga_harian (kode_kota, komoditas_id, tanggal)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS history_data_komoditas_monthly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode_kota VARCHAR(50) NOT NULL,
        nama_kota VARCHAR(100) NOT NULL,
        komoditas_id INT NOT NULL,
        komoditas_nama VARCHAR(150) NOT NULL,
        harga_ratarata INT NOT NULL,
        harga_tertinggi INT NOT NULL,
        harga_terendah INT NOT NULL,
        bulan INT NOT NULL,
        tahun INT NOT NULL,
        cnt_hari INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_harga_bulanan (kode_kota, komoditas_id, bulan, tahun)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecast_harga_komoditas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode_kota VARCHAR(50) NOT NULL,
        komoditas_id INT NOT NULL,
        komoditas_nama VARCHAR(150) NOT NULL,
        model VARCHAR(10) NOT NULL, -- SES / DES
        mae float(25) NOT NULL,
        mape float(25) NOT NULL,
        rmse float(25) NOT NULL,
        tanggal DATE NOT NULL,
        harga_prediksi INT NOT NULL,
        normalized float NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_forecast (
            kode_kota, komoditas_id, model, tanggal
        )
    );
    """,
]

# Backfill data beras lama (tipe premium/medium) -> komoditas_id (2/4), bila
# tabel lama masih ada. Idempotent lewat ON DUPLICATE KEY / INSERT IGNORE.
BACKFILL = [
    ("history_data_beras", """
        INSERT IGNORE INTO history_data_komoditas
            (kode_kota, nama_kota, komoditas_id, komoditas_nama, harga, tanggal)
        SELECT
            kode_kota, nama_kota,
            CASE tipe WHEN 'premium' THEN 2 WHEN 'medium' THEN 4 END,
            CASE tipe WHEN 'premium' THEN 'Beras Premium' WHEN 'medium' THEN 'Beras Medium' END,
            harga, tanggal
        FROM history_data_beras
        WHERE tipe IN ('premium', 'medium')
    """),
    ("history_data_beras_monthly", """
        INSERT IGNORE INTO history_data_komoditas_monthly
            (kode_kota, nama_kota, komoditas_id, komoditas_nama,
             harga_ratarata, harga_tertinggi, harga_terendah, bulan, tahun, cnt_hari)
        SELECT
            kode_kota, nama_kota,
            CASE tipe WHEN 'premium' THEN 2 WHEN 'medium' THEN 4 END,
            CASE tipe WHEN 'premium' THEN 'Beras Premium' WHEN 'medium' THEN 'Beras Medium' END,
            harga_ratarata, harga_tertinggi, harga_terendah, bulan, tahun, cnt_hari
        FROM history_data_beras_monthly
        WHERE tipe IN ('premium', 'medium')
    """),
]


def create_database():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))


def create_tables():
    engine = get_engine(DB_NAME)
    with engine.begin() as conn:
        for table_sql in TABLES:
            conn.execute(text(table_sql))


def _table_exists(conn, table_name: str) -> bool:
    row = conn.execute(
        text("""
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = :db AND table_name = :tbl
        """),
        {"db": DB_NAME, "tbl": table_name},
    ).scalar()
    return bool(row)


def backfill_beras():
    """Salin data beras lama ke tabel komoditas (aman dijalankan berulang)."""
    engine = get_engine(DB_NAME)
    with engine.begin() as conn:
        for old_table, sql in BACKFILL:
            if _table_exists(conn, old_table):
                result = conn.execute(text(sql))
                logger.info(
                    f"Backfill {old_table} -> komoditas | rows={result.rowcount}"
                )


def run_migrations():
    create_database()
    create_tables()
    backfill_beras()
    print("Database dan tabel komoditas siap (SQLAlchemy).")


if __name__ == "__main__":
    run_migrations()
