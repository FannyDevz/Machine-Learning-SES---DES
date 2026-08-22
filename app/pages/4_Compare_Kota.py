import streamlit as st

from app.uikit.ui import setup_page, hero, pilih_kota_multi, pilih_komoditas
from app.uikit import charts
from analytics.compare import load_compare_data

setup_page("Perbandingan Kota", icon="🏙️")
hero("🏙️ Perbandingan Harga Antar Kota", "Bandingkan harga satu komoditas di beberapa kota sekaligus.")

# ---- Filter ----------------------------------------------------------------
with st.container(border=True):
    kota_list = pilih_kota_multi("Pilih Kota (minimal 2)", default_n=2)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        komoditas_id, komoditas_nama = pilih_komoditas()
    with c2:
        start_date = st.date_input("Tanggal Mulai")
    with c3:
        end_date = st.date_input("Tanggal Akhir")

if len(kota_list) < 2:
    st.warning("Pilih minimal 2 kota untuk dibandingkan.")
    st.stop()

df = load_compare_data(kota_list, komoditas_id, start_date, end_date)

if df.empty:
    st.warning("Data tidak ditemukan untuk filter ini.")
    st.stop()

st.markdown(f"<span class='badge'>{komoditas_nama}</span>", unsafe_allow_html=True)

# ---- Grafik ----------------------------------------------------------------
st.subheader("Grafik Perbandingan")
st.plotly_chart(charts.compare_lines(df, kota_list), use_container_width=True)

# ---- Statistik -------------------------------------------------------------
st.subheader("Statistik Ringkas per Kota")
summary = (
    df.groupby("kode_kota")["harga"]
    .agg(Rata_rata="mean", Minimum="min", Maksimum="max")
    .round(0)
    .reset_index()
    .rename(columns={"kode_kota": "Kota"})
)
st.dataframe(
    summary,
    use_container_width=True,
    column_config={
        "Rata_rata": st.column_config.NumberColumn("Rata-rata", format="Rp %d"),
        "Minimum": st.column_config.NumberColumn("Minimum", format="Rp %d"),
        "Maksimum": st.column_config.NumberColumn("Maksimum", format="Rp %d"),
    },
)
