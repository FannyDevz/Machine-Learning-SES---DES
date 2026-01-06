import pandas as pd
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME


def save_forecast_to_db(
    kode_kota: str,
    tipe: str,
    model: str,
    mae: float,
    mape: float,
    rmse: float,
    dates: pd.DatetimeIndex,
    values: pd.Series,
    normalized: float
):
    engine = get_engine(DB_NAME)

    df = pd.DataFrame({
        "kode_kota": kode_kota,
        "tipe": tipe,
        "model": model,
        "mae": mae,
        "mape": mape,
        "rmse": rmse,
        "tanggal": dates.date,
        "harga_prediksi": values.round().astype(int),
        "normalized": normalized
    })

    query = text("""
        INSERT INTO forecast_harga_beras
            (kode_kota, tipe, model,  mae, mape, rmse, tanggal, harga_prediksi, normalized)
        VALUES
            (:kode_kota, :tipe, :model,:mae, :mape, :rmse,  :tanggal, :harga_prediksi, :normalized)
        ON DUPLICATE KEY UPDATE
            harga_prediksi = VALUES(harga_prediksi),
            mae = VALUES(mae),
            mape = VALUES(mape),
            rmse = VALUES(rmse),
            normalized = VALUES(normalized),
            created_at = CURRENT_TIMESTAMP
    """)

    with engine.begin() as conn:
        conn.execute(query, df.to_dict(orient="records"))
