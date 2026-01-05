from sqlalchemy import create_engine
from config.settings import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_PORT,
)

def get_engine(db_name: str | None = None):
    """
    Membuat SQLAlchemy engine.
    Jika db_name None → koneksi tanpa database (untuk create DB).
    """
    database = db_name if db_name else ''
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{database}"

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    return engine
