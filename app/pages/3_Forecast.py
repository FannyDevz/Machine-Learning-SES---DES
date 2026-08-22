import streamlit as st

from app.uikit.ui import setup_page, hero, stat_cards, pilih_kota, pilih_komoditas
from app.uikit import charts
from forecast.dataset import load_monthly_series
from forecast.split import train_test_split_ts
from forecast.normalize import minmax_scale, minmax_inverse
from forecast.ses import fit_ses
from forecast.des import fit_des
from forecast.auto_select import auto_select_model
from forecast.evaluate import mae, mape, rmse

setup_page("Forecast", icon="📈")
hero("📈 Forecast Harga Komoditas", "Prediksi dengan Single/Double Exponential Smoothing (SES/DES).")

# ---- Filter ----------------------------------------------------------------
with st.container(border=True):
    c1, c2 = st.columns(2)
    with c1:
        kode_kota = pilih_kota()
    with c2:
        komoditas_id, komoditas_nama = pilih_komoditas()

    c3, c4 = st.columns([2, 1])
    with c3:
        model_choice = st.radio(
            "Model", ["Auto (SES vs DES)", "SES", "DES"], horizontal=True
        )
    with c4:
        train_percent = st.slider("Data Training (%)", 60, 90, 80)

st.markdown(f"<span class='badge'>{komoditas_nama} · {kode_kota}</span>", unsafe_allow_html=True)

# ---- Load & split ----------------------------------------------------------
try:
    series = load_monthly_series(kode_kota, komoditas_id)
except ValueError as e:
    st.warning(f"{e}")
    st.stop()

if len(series) < 6:
    st.warning(f"Data bulanan terlalu sedikit ({len(series)} titik) untuk forecast.")
    st.stop()

train_size = int(len(series) * train_percent / 100)
test_size = len(series) - train_size
train, test = train_test_split_ts(series, test_size)

# Normalisasi (fit di train saja)
train_scaled, min_val, max_val = minmax_scale(train)
test_scaled = (test - min_val) / (max_val - min_val)

# ---- Forecast ---------------------------------------------------------------
if model_choice == "SES":
    _, fc_scaled = fit_ses(train_scaled, len(test))
    model_name = "SES"
elif model_choice == "DES":
    _, fc_scaled = fit_des(train_scaled, len(test))
    model_name = "DES"
else:
    result = auto_select_model(train_scaled, test_scaled)
    fc_scaled = result["forecast"]
    model_name = result["model"]

m_mae = mae(test_scaled, fc_scaled)
m_mape = mape(test_scaled, fc_scaled)
m_rmse = rmse(test_scaled, fc_scaled)
fc_rupiah = minmax_inverse(fc_scaled, min_val, max_val)

# ---- Metrik -----------------------------------------------------------------
stat_cards([
    {"label": "Model Terpilih", "value": model_name, "accent": True},
    {"label": "MAPE", "value": f"{m_mape:.2f}%"},
    {"label": "RMSE", "value": f"{m_rmse:.4f}"},
    {"label": "MAE", "value": f"{m_mae:.4f}"},
])
st.caption("Metrik dihitung pada skala ternormalisasi (0–1). Grafik ditampilkan dalam Rupiah.")

# ---- Grafik -----------------------------------------------------------------
st.subheader(f"Hasil Forecast — {model_name}")
st.plotly_chart(
    charts.forecast_chart(train, test, fc_rupiah),
    use_container_width=True,
)

st.caption(
    f"Total data: {len(series)} bulan · Train: {len(train)} · Test: {len(test)}"
)
