import streamlit as st

from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

from analytics.daily.dataset import load_daily_data
from analytics.daily.stats import daily_stats
from analytics.daily.change import daily_change
from analytics.daily.outlier import detect_spike
from analytics.daily.plot import plot_daily_price


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

st.title("📊 Analitik Harga Harian")

kode_kota = st.selectbox("Kota", get_daftar_kota())
tipe = st.radio("Tipe Beras", ["medium", "premium"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Tanggal Mulai")
with col2:
    end = st.date_input("Tanggal Akhir")

df = load_daily_data(kode_kota, tipe, start, end)

# =====================
# Statistik
# =====================
stats = daily_stats(df)

st.metric("Harga Minimum", stats["min"])
st.metric("Harga Maksimum", stats["max"])
st.metric("Rata-rata", round(stats["mean"], 2))

# =====================
# Grafik
# =====================
st.pyplot(plot_daily_price(df))

# =====================
# Perubahan Harian
# =====================
df_change = daily_change(df)
st.subheader("📉 Perubahan Harian")
st.dataframe(df_change.tail(100))

# =====================
# Lonjakan Harga
# =====================
spike = detect_spike(df, threshold_pct=5)
if not spike.empty:
    st.warning("🚨 Terdeteksi lonjakan harga!")
    st.dataframe(spike)
else:
    st.success("Tidak ada lonjakan signifikan")
