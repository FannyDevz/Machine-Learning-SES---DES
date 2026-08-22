import streamlit as st

from app.utils.ui import setup_page, hero, stat_cards, format_rupiah
from app.services.data_service import get_overview

setup_page("Dashboard Harga Komoditas", icon="📊")

hero(
    "📊 Dashboard Harga Komoditas Jawa Timur",
    "Pantau, analisis, dan prediksi harga berbagai komoditas pangan & non-pangan "
    "berdasarkan kota dan waktu.",
)

# ---- Ringkasan data --------------------------------------------------------
try:
    ov = get_overview()
except Exception:
    ov = {}

if ov and ov.get("total_baris"):
    def _fmt(n):
        return f"{int(n):,}".replace(",", ".")

    rentang = "—"
    if ov.get("tgl_awal") and ov.get("tgl_akhir"):
        rentang = f"{ov['tgl_awal']:%b %Y} – {ov['tgl_akhir']:%b %Y}"

    stat_cards([
        {"label": "Total Komoditas", "value": _fmt(ov["total_komoditas"]), "accent": True},
        {"label": "Total Kota", "value": _fmt(ov["total_kota"])},
        {"label": "Baris Data Harian", "value": _fmt(ov["total_baris"])},
        {"label": "Rentang Data", "value": rentang.split(" – ")[0], "sub": f"s/d {rentang.split(' – ')[-1]}"},
    ])
else:
    st.info(
        "Database masih kosong. Buka halaman **🔄 Fetch Data** di sidebar untuk "
        "mengambil data komoditas pertama Anda."
    )

# ---- Panduan navigasi ------------------------------------------------------
st.subheader("Menu")

c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "**🔄 Fetch Data** — ambil data komoditas dari SISKAPERBAPO & agregasi bulanan.\n\n"
        "**📊 Analitik Harian** — statistik, tren, dan deteksi lonjakan harga harian."
    )
with c2:
    st.markdown(
        "**📅 Agregasi Bulanan** — ringkasan & perubahan harga bulan-ke-bulan.\n\n"
        "**📈 Forecast** — prediksi harga dengan Exponential Smoothing (SES/DES).\n\n"
        "**🏙️ Perbandingan Kota** — bandingkan harga satu komoditas antar kota."
    )

st.caption("Sumber data: siskaperbapo.jatimprov.go.id · Model: SES & DES (statsmodels)")
