import streamlit as st

from app.uikit.ui import setup_page, hero, stat_cards, format_rupiah, pilih_kota, pilih_komoditas
from app.uikit import charts
from analytics.monthly.dataset import load_monthly_data
from analytics.monthly.stats import monthly_summary
from analytics.monthly.change import monthly_change

setup_page("Agregasi Bulanan", icon="📅")
hero("📅 Agregasi Bulanan", "Ringkasan dan perubahan harga bulan-ke-bulan (MoM) per kota & komoditas.")

# ---- Filter ----------------------------------------------------------------
with st.container(border=True):
    c1, c2 = st.columns(2)
    with c1:
        kode_kota = pilih_kota()
    with c2:
        komoditas_id, komoditas_nama = pilih_komoditas()
    c3, c4 = st.columns(2)
    with c3:
        start_year = st.number_input("Tahun Mulai", 2020, 2030, 2022)
    with c4:
        end_year = st.number_input("Tahun Akhir", 2020, 2030, 2025)

df = load_monthly_data(kode_kota, komoditas_id, start_year, end_year)

if df.empty:
    st.warning("Data bulanan tidak ditemukan. Jalankan agregasi di halaman **🔄 Fetch Data**.")
    st.stop()

st.markdown(f"<span class='badge'>{komoditas_nama} · {kode_kota}</span>", unsafe_allow_html=True)

# ---- Statistik -------------------------------------------------------------
summary = monthly_summary(df)
stat_cards([
    {"label": "Rata-rata", "value": format_rupiah(summary["avg"]), "accent": True},
    {"label": "Tertinggi", "value": format_rupiah(summary["max"]),
     "sub": f"{summary['bulan_termahal']:%b %Y}"},
    {"label": "Terendah", "value": format_rupiah(summary["min"]),
     "sub": f"{summary['bulan_termurah']:%b %Y}"},
    {"label": "Jumlah Bulan", "value": str(len(df))},
])

# ---- Grafik ----------------------------------------------------------------
st.subheader("Tren Harga Bulanan")
st.plotly_chart(charts.monthly_band(df), use_container_width=True)

# ---- MoM -------------------------------------------------------------------
st.subheader("📉 Perubahan Bulanan (MoM)")
df_change = monthly_change(df)
st.dataframe(
    df_change[["harga_ratarata", "mom_change", "mom_pct", "cnt_hari"]],
    use_container_width=True,
    column_config={
        "harga_ratarata": st.column_config.NumberColumn("Rata-rata", format="Rp %d"),
        "mom_change": st.column_config.NumberColumn("Δ MoM", format="Rp %d"),
        "mom_pct": st.column_config.NumberColumn("Δ %", format="%.2f%%"),
        "cnt_hari": st.column_config.NumberColumn("Jml Hari"),
    },
)
