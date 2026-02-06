import streamlit as st
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

from forecast.dataset import load_monthly_series
from forecast.split import train_test_split_ts
from forecast.normalize import minmax_scale, minmax_inverse
from forecast.ses import fit_ses
from forecast.des import fit_des
from forecast.auto_select import auto_select_model
from forecast.evaluate import mape, rmse
from forecast.plot_streamlit import plot_forecast

# ===============================
# Helper: ambil daftar kota
# ===============================

def get_daftar_kota():
    engine = get_engine(DB_NAME)
    query = text("""
        SELECT DISTINCT kode_kota
        FROM history_data_beras
        ORDER BY kode_kota
    """)
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(query).fetchall()]

# ===============================
# UI
# ===============================
st.title("📈 Forecast Harga Beras")

kode_kota = st.selectbox("Kota", get_daftar_kota())
tipe = st.radio("Tipe Beras", ["medium", "premium"], horizontal=True)

model_choice = st.radio(
    "Model Forecast",
    ["Auto (SES vs DES)", "SES", "DES"],
    horizontal=True
)

train_percent = st.slider(
    "Persentase Data Training (%)",
    min_value=60,
    max_value=90,
    value=80
)

# ===============================
# Load & split data
# ===============================
series = load_monthly_series(kode_kota, tipe)

train_size = int(len(series) * train_percent / 100)
test_size = len(series) - train_size

train, test = train_test_split_ts(series, test_size)

# ===============================
# Normalisasi (fit di train saja)
# ===============================
train_scaled, min_val, max_val = minmax_scale(train)
test_scaled = (test - min_val) / (max_val - min_val)

# ===============================
# Forecasting
# ===============================
st.subheader("📊 Hasil Forecast")

if model_choice == "SES":
    _, ses_forecast_scaled = fit_ses(train_scaled, len(test))
    st.write("### Single Exponential Smoothing (SES)")
    st.write("MAPE:", mape(test_scaled, ses_forecast_scaled)),"%"
    st.write("RMSE:", rmse(test_scaled, ses_forecast_scaled))
    fig = plot_forecast(train_scaled, test_scaled, ses_forecast_scaled, "SES Forecast Normalized")
    st.pyplot(fig)
    
    ses_forecast = minmax_inverse(ses_forecast_scaled, min_val, max_val)
    
    fig = plot_forecast(train, test, ses_forecast, "SES Forecast ")
    st.pyplot(fig)

elif model_choice == "DES":
    _, des_forecast_scaled = fit_des(train_scaled, len(test))
    st.write("### Double Exponential Smoothing (DES)")
    st.write("MAPE:", mape(test_scaled, des_forecast_scaled)) ,"%"
    st.write("RMSE:", rmse(test_scaled, des_forecast_scaled))
    fig = plot_forecast(train_scaled, test_scaled, des_forecast_scaled, "DES Forecast")
    st.pyplot(fig)
    
    des_forecast = minmax_inverse(des_forecast_scaled, min_val, max_val)
    
    fig = plot_forecast(train, test, des_forecast, "DES Forecast ")
    st.pyplot(fig)

else:
    result = auto_select_model(train_scaled, test_scaled)

    st.success(f"""
    Model Terpilih: **{result['model']}**  
    MAPE: {result['mape']:.2f}  %
    RMSE: {result['rmse']:.2f}
    """)

        
    fig = plot_forecast(
        train_scaled,
        test_scaled,
        result["forecast"],
        f"Auto Forecast ({result['model']}) Normalized" 
    )
    st.pyplot(fig)
    
    frcst = minmax_inverse(result["forecast"], min_val, max_val)
        
    fig = plot_forecast(
        train,
        test,
        frcst,
        f"Auto Forecast ({result['model']})"
    )
    st.pyplot(fig)


# ===============================
# Info tambahan
# ===============================
st.caption(
    f"""
    Data points: {len(series)}  
    Train: {len(train)} | Test: {len(test)}
    """
)
