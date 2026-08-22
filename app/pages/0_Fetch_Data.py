import streamlit as st
from datetime import date

from app.uikit.ui import setup_page, hero, stat_cards
from etl.extract import extract_range
from etl.transform import transform_data
from etl.load import load_to_db
from etl.aggregate import aggregate_monthly
from etl.komoditas import get_catalog
from utils.logger import logger

setup_page("Fetch Data", icon="🔄")
hero(
    "🔄 Fetch Data Komoditas",
    "Ambil harga berbagai komoditas dari SISKAPERBAPO Jawa Timur "
    "(Extract → Transform → Load), lalu agregasi ke bulanan.",
)

catalog = get_catalog()  # {id: nama}
nama_ke_id = {nama: kid for kid, nama in catalog.items()}

# ===============================
# 1. Fetch data harian
# ===============================
st.subheader("1️⃣ Ambil Data Harian")

with st.container(border=True):
    pilihan_komoditas = st.multiselect(
        "Pilih Komoditas",
        options=list(nama_ke_id.keys()),
        default=["Beras Premium", "Beras Medium"],
        help="Semakin banyak komoditas & rentang tanggal, semakin lama prosesnya.",
    )
    komoditas_ids = [nama_ke_id[n] for n in pilihan_komoditas]

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Tanggal Mulai", value=date.today())
    with col2:
        end_date = st.date_input("Tanggal Akhir", value=date.today())

    if start_date > end_date:
        st.warning("Tanggal mulai tidak boleh lebih besar dari tanggal akhir.")
    if not komoditas_ids:
        st.info("Pilih minimal satu komoditas untuk diambil.")

    fetch_disabled = start_date > end_date or not komoditas_ids
    do_fetch = st.button("🚀 Ambil & Simpan Data", type="primary", disabled=fetch_disabled)

if do_fetch:
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    try:
        with st.spinner(
            f"Mengambil {len(komoditas_ids)} komoditas | {start_str} s/d {end_str}..."
        ):
            df_raw = extract_range(
                start_date=start_str, end_date=end_str, komoditas_ids=komoditas_ids
            )

        if df_raw.empty:
            st.error("Tidak ada data yang berhasil diambil untuk rentang ini.")
        else:
            df_clean = transform_data(df_raw)
            with st.spinner("Menyimpan ke database..."):
                load_to_db(df_clean)
            logger.info(f"ETL via UI selesai | total_rows={len(df_clean)}")

            st.success("Data berhasil diambil & disimpan.")
            stat_cards([
                {"label": "Baris Diambil", "value": f"{len(df_raw):,}".replace(",", "."), "accent": True},
                {"label": "Baris Tersimpan", "value": f"{len(df_clean):,}".replace(",", ".")},
                {"label": "Komoditas", "value": str(df_clean['komoditas_id'].nunique())},
                {"label": "Kota", "value": str(df_clean['kode_kota'].nunique())},
            ])

            tab1, tab2 = st.tabs(["📋 Preview", "📦 Per Komoditas"])
            with tab1:
                st.dataframe(df_clean.head(100), use_container_width=True)
            with tab2:
                st.dataframe(
                    df_clean["komoditas_nama"].value_counts().rename("jumlah_baris"),
                    use_container_width=True,
                )
    except Exception as e:
        logger.error(f"Fetch via UI gagal | error={e}")
        st.error(f"Gagal mengambil data: {e}")

st.divider()

# ===============================
# 2. Agregasi bulanan
# ===============================
st.subheader("2️⃣ Agregasi ke Bulanan")
st.caption(
    "Isi tabel bulanan (dipakai halaman Agregasi Bulanan & Forecast) dari data harian."
)

with st.container(border=True):
    col3, col4 = st.columns(2)
    with col3:
        start_year = st.number_input("Tahun Mulai", 2020, 2030, date.today().year)
    with col4:
        end_year = st.number_input("Tahun Akhir", 2020, 2030, date.today().year)

    agg = st.button("📅 Jalankan Agregasi Bulanan", disabled=start_year > end_year)

if agg:
    try:
        with st.spinner(f"Agregasi bulanan {start_year}–{end_year}..."):
            aggregate_monthly(start_year=int(start_year), end_year=int(end_year))
        st.success("Agregasi bulanan selesai.")
    except Exception as e:
        logger.error(f"Agregasi via UI gagal | error={e}")
        st.error(f"Gagal melakukan agregasi: {e}")
