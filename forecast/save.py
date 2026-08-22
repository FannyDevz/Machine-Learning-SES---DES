import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME
from etl.komoditas import komoditas_nama as _komoditas_nama


def save_forecast_to_db(
    kode_kota: str,
    komoditas_id: int,
    model: str,
    mae: float,
    mape: float,
    rmse: float,
    dates: pd.DatetimeIndex,
    values: pd.Series,
    normalized: float,
    komoditas_nama: str | None = None
):
    engine = get_engine(DB_NAME)

    if komoditas_nama is None:
        komoditas_nama = _komoditas_nama(komoditas_id)

    df = pd.DataFrame({
        "kode_kota": kode_kota,
        "komoditas_id": int(komoditas_id),
        "komoditas_nama": komoditas_nama,
        "model": model,
        "mae": mae,
        "mape": mape,
        "rmse": rmse,
        "tanggal": dates.date,
        "harga_prediksi": values.round().astype(int),
        "normalized": normalized
    })

    query = text("""
        INSERT INTO forecast_harga_komoditas
            (kode_kota, komoditas_id, komoditas_nama, model, mae, mape, rmse,
             tanggal, harga_prediksi, normalized)
        VALUES
            (:kode_kota, :komoditas_id, :komoditas_nama, :model, :mae, :mape, :rmse,
             :tanggal, :harga_prediksi, :normalized)
        ON DUPLICATE KEY UPDATE
            komoditas_nama = VALUES(komoditas_nama),
            harga_prediksi = VALUES(harga_prediksi),
            mae = VALUES(mae),
            mape = VALUES(mape),
            rmse = VALUES(rmse),
            normalized = VALUES(normalized),
            created_at = CURRENT_TIMESTAMP
    """)

    with engine.begin() as conn:
        conn.execute(query, df.to_dict(orient="records"))
