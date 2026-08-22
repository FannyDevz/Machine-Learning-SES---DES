import streamlit as st

from app.uikit.ui import setup_page, hero, stat_cards, format_rupiah, pilih_kota, pilih_komoditas
from app.uikit import charts
from analytics.daily.dataset import load_daily_data
from analytics.daily.stats import daily_stats
from analytics.daily.change import daily_change
from analytics.daily.outlier import detect_spike

setup_page("Analitik Harian", icon="📊")
hero("📊 Analitik Harga Harian", "Statistik, tren, dan deteksi lonjakan harga per kota & komoditas.")

# ---- Filter ----------------------------------------------------------------
with st.container(border=True):
    c1, c2 = st.columns(2)
    with c1:
        kode_kota = pilih_kota()
    with c2:
        komoditas_id, komoditas_nama = pilih_komoditas()
    c3, c4 = st.columns(2)
    with c3:
        start = st.date_input("Tanggal Mulai")
    with c4:
        end = st.date_input("Tanggal Akhir")

df = load_daily_data(kode_kota, komoditas_id, start, end)

if df.empty:
    st.warning("Data tidak ditemukan untuk filter ini.")
    st.stop()

st.markdown(f"<span class='badge'>{komoditas_nama} · {kode_kota}</span>", unsafe_allow_html=True)

# ---- Statistik -------------------------------------------------------------
s = daily_stats(df)
stat_cards([
    {"label": "Rata-rata", "value": format_rupiah(s["mean"]), "accent": True},
    {"label": "Tertinggi", "value": format_rupiah(s["max"])},
    {"label": "Terendah", "value": format_rupiah(s["min"])},
    {"label": "Median", "value": format_rupiah(s["median"])},
])

# ---- Grafik ----------------------------------------------------------------
st.subheader("Tren Harga Harian")
plot_df = df.reset_index()
st.plotly_chart(
    charts.line_price(plot_df, x="tanggal", y="harga", name=komoditas_nama),
    use_container_width=True,
)

# ---- Detail ----------------------------------------------------------------
tab1, tab2 = st.tabs(["🚨 Lonjakan Harga", "📉 Perubahan Harian"])

with tab1:
    spike = detect_spike(df, threshold_pct=5)
    if not spike.empty:
        st.warning(f"Terdeteksi {len(spike)} lonjakan harga (≥5%).")
        st.dataframe(spike, use_container_width=True)
    else:
        st.success("Tidak ada lonjakan signifikan (≥5%).")

with tab2:
    df_change = daily_change(df)
    st.dataframe(df_change.tail(100), use_container_width=True)
