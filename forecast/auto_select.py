from forecast.ses import fit_ses
from forecast.des import fit_des
from forecast.evaluate import mae, rmse,mape

def auto_select_model(train_scaled, test_scaled, min_val, max_val, metric="mape"):
    """
    Menghitung forecast pada data scaled, dan mengembalikan metrik 
    dalam dua skala: Scaled (0-1) dan Asli (Rupiah).
    """
    from forecast.normalize import minmax_inverse
    import numpy as np

    # --- Persiapan Data Asli untuk Evaluasi ---
    test_asli = minmax_inverse(test_scaled, min_val, max_val)

    # --- Perhitungan SES ---
    _, ses_forecast_scaled = fit_ses(train_scaled, len(test_scaled))
    ses_forecast_asli = minmax_inverse(ses_forecast_scaled, min_val, max_val)
    
    # Metrik SES
    ses_mape = mape(test_asli, ses_forecast_asli) # MAPE wajib dari data asli
    ses_rmse_scaled = rmse(test_scaled, ses_forecast_scaled) # RMSE skala 0-1
    ses_rmse_asli = rmse(test_asli, ses_forecast_asli) # RMSE skala Rupiah

    # --- Perhitungan DES ---
    _, des_forecast_scaled = fit_des(train_scaled, len(test_scaled))
    des_forecast_asli = minmax_inverse(des_forecast_scaled, min_val, max_val)
    
    # Metrik DES
    des_mape = mape(test_asli, des_forecast_asli)
    des_rmse_scaled = rmse(test_scaled, des_forecast_scaled)
    des_rmse_asli = rmse(test_asli, des_forecast_asli)

    # --- Logika Pemilihan Model ---
    # Gunakan MAPE atau RMSE Scaled sebagai penentu model terbaik
    if metric == "rmse":
        ses_score, des_score = ses_rmse_scaled, des_rmse_scaled
    else:
        ses_score, des_score = ses_mape, des_mape

    if ses_score <= des_score:
        return {
            "model": "SES",
            "forecast_scaled": ses_forecast_scaled,
            "mape": ses_mape,
            "rmse_scaled": ses_rmse_scaled,
            "rmse_asli": ses_rmse_asli
        }
    else:
        return {
            "model": "DES",
            "forecast_scaled": des_forecast_scaled,
            "mape": des_mape,
            "rmse_scaled": des_rmse_scaled,
            "rmse_asli": des_rmse_asli
        }