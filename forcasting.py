from forecast.dataset import load_monthly_series
from forecast.split import train_test_split_ts
from forecast.ses import fit_ses
from forecast.des import fit_des
from forecast.evaluate import mae, mape, rmse
from forecast.plot import plot_forecast
from forecast.normalize import minmax_scale, minmax_inverse
from forecast.utils import generate_future_dates
from forecast.save import save_forecast_to_db
from utils.logger import logger
from database.queries import get_kode_kota_type


def main(kode_kota ,tipe):
    horizon = 6  # prediksi 6 bulan ke depan
    
    series = load_monthly_series(kode_kota, tipe)

    test_size = len(series) // 5  # 20% test

    train, test = train_test_split_ts(series, test_size=test_size)

    print("Train length:", len(train))
    print("Test length:", len(test))

    # ======================
    # NORMALISASI (FIT DI TRAIN SAJA)
    # ======================
    train_scaled, min_val, max_val = minmax_scale(train)

    # transform test pakai min/max train
    test_scaled = (test - min_val) / (max_val - min_val)

    # ======================
    # SES
    # ======================
    _, ses_forecast_scaled = fit_ses(train_scaled, len(test))

    # ======================
    # DES
    # ======================
    _, des_forecast_scaled = fit_des(train_scaled, len(test))

    # ======================
    # EVALUASI (SCALE SPACE)
    # ======================
    ses_mae = mae(test_scaled, ses_forecast_scaled)
    ses_mape = mape(test_scaled, ses_forecast_scaled)
    ses_rmse = rmse(test_scaled, ses_forecast_scaled)
    des_mae = mae(test_scaled, des_forecast_scaled)
    des_mape = mape(test_scaled, des_forecast_scaled)
    des_rmse = rmse(test_scaled, des_forecast_scaled)
    
    print("SES MAE:", ses_mae)
    print("DES MAE:", des_mae)

    print("SES MAPE:", ses_mape)
    print("DES MAPE:", des_mape)

    print("SES RMSE:", ses_rmse)
    print("DES RMSE:", des_rmse)

    # ======================
    # INVERSE KE RUPIAH
    # ======================
    ses_forecast = minmax_inverse(ses_forecast_scaled, min_val, max_val)
    des_forecast = minmax_inverse(des_forecast_scaled, min_val, max_val)

    # ======================
    # PLOT (RUPIAH)
    # ======================
    
    # plot_forecast(train, test, ses_forecast, "SES Forecast (Rp)")
    # plot_forecast(train, test, des_forecast, "DES Forecast (Rp)")
    
    # plot_forecast(train_scaled, test_scaled, ses_forecast_scaled, "SES Forecast (Normaized)")
    # plot_forecast(train_scaled, test_scaled, des_forecast_scaled, "DES Forecast (Normaized) ")


    future_dates = generate_future_dates(series.index[-1], len(test))
    # ===== SIMPAN KE DB =====
    save_forecast_to_db(
        kode_kota, tipe, "SES", ses_mae,  ses_mape, ses_rmse,
        future_dates, ses_forecast , ses_forecast_scaled
    )

    save_forecast_to_db(
        kode_kota, tipe, "DES",  des_mae,  des_mape, des_rmse,
        future_dates, des_forecast, des_forecast_scaled
    )
    
if __name__ == "__main__":
    daftar_kombinasi = get_kode_kota_type() 
    
    for kode_kota, tipe in daftar_kombinasi:
        print(f"Memproses {kode_kota} - {tipe}...")
        try:
            main(kode_kota, tipe)
        except Exception as e:
            logger.error(f"{kode_kota}-{tipe} gagal: {e}")

