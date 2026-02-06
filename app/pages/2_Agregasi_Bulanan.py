import streamlit as st

from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

from analytics.monthly.dataset import load_monthly_data
from analytics.monthly.stats import monthly_summary
from analytics.monthly.change import monthly_change
from analytics.monthly.plot import plot_monthly_trend

def get_daftar_kota():
    engine = get_engine(DB_NAME)
    query = text("""
        SELECT DISTINCT kode_kota
        FROM history_data_beras
        ORDER BY kode_kota
    """)
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(query).fetchall()]


st.title("📅 Agregasi Bulanan Harga Beras")

kode_kota = st.selectbox("Kota", get_daftar_kota())
tipe = st.radio("Tipe Beras", ["medium", "premium"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    start_year = st.number_input("Tahun Mulai", 2020, 2030, 2022)
with col2:
    end_year = st.number_input("Tahun Akhir", 2020, 2030, 2025)

df = load_monthly_data(kode_kota, tipe, start_year, end_year)

# =====================
# Statistik Ringkas
# =====================
summary = monthly_summary(df)

st.metric("Rata-rata Harga", int(summary["avg"]))
st.metric("Harga Tertinggi", int(summary["max"]))
st.metric("Harga Terendah", int(summary["min"]))

# =====================
# Grafik
# =====================
st.pyplot(
    plot_monthly_trend(
        df,
        f"Harga Bulanan {kode_kota.upper()} ({tipe})"
    )
)

# =====================
# MoM Change
# =====================
st.subheader("📉 Perubahan Bulanan (MoM)")
df_change = monthly_change(df)
## Harga Rata RAta | Monthly Change | Monthly Persentase Change | Jumlah Hari
st.dataframe(df_change[[
    "harga_ratarata", "mom_change", "mom_pct", "cnt_hari"
]])
