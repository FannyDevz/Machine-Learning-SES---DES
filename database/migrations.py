from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

TABLES = [
    """
    CREATE TABLE IF NOT EXISTS history_data_beras (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode_kota VARCHAR(50) NOT NULL,
        nama_kota VARCHAR(100) NOT NULL,
        tipe VARCHAR(10) NOT NULL,
        harga INT NOT NULL,
        tanggal DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_harga_harian (kode_kota, tipe, tanggal)
    );
    """,
    """
        CREATE TABLE IF NOT EXISTS history_data_beras_monthly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode_kota VARCHAR(50) NOT NULL,
        nama_kota VARCHAR(100) NOT NULL,
        tipe VARCHAR(10) NOT NULL,
        harga_ratarata INT NOT NULL,
        harga_tertinggi INT NOT NULL,
        harga_terendah INT NOT NULL,
        bulan INT NOT NULL,
        tahun INT NOT NULL,
        cnt_hari INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_harga_bulanan (kode_kota, tipe, bulan, tahun)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecast_harga_beras (
        id INT AUTO_INCREMENT PRIMARY KEY,
        kode_kota VARCHAR(50) NOT NULL,
        tipe VARCHAR(10) NOT NULL,
        model VARCHAR(10) NOT NULL, -- SES / DES
        mae float(25) NOT NULL,
        mape float(25) NOT NULL,
        rmse float(25) NOT NULL,
        tanggal DATE NOT NULL,
        harga_prediksi INT NOT NULL,
        normalized float NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uniq_forecast (
            kode_kota, tipe, model, tanggal
        )
    );
    """
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

def run_migrations():
    create_database()
    create_tables()
    print("Database dan tabel siap (SQLAlchemy).")

if __name__ == "__main__":
    run_migrations()
