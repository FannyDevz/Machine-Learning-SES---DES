# app/pages/4_Compare_Kota.py
import streamlit as st
import matplotlib.pyplot as plt

from analytics.compare import load_compare_data
from sqlalchemy import text
from database.connection import get_engine
from config.settings import DB_NAME

# ===============================
# Helper: daftar kota
# ===============================
@st.cache_data
def get_kota():
    engine = get_engine(DB_NAME)
    q = text("SELECT DISTINCT kode_kota FROM history_data_beras ORDER BY kode_kota")
    with engine.connect() as c:
        return [r[0] for r in c.execute(q)]

# ===============================
# UI
# ===============================
st.title("🏙️ Perbandingan Harga Antar Kota")

kota_list = st.multiselect(
    "Pilih Kota (minimal 2)",
    get_kota(),
    default=["surabayakota", "bangkalankab"]
)

tipe = st.radio("Tipe Beras", ["medium", "premium"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Tanggal Mulai")
with col2:
    end_date = st.date_input("Tanggal Akhir")

if len(kota_list) < 2:
    st.warning("Pilih minimal 2 kota untuk dibandingkan.")
    st.stop()

# ===============================
# Load data
# ===============================
df = load_compare_data(
    kota_list,
    tipe,
    start_date,
    end_date
)

if df.empty:
    st.warning("Data tidak ditemukan.")
    st.stop()

# ===============================
# Plot
# ===============================
st.subheader("📈 Grafik Perbandingan Harga")

fig, ax = plt.subplots(figsize=(10, 4))

for kota in kota_list:
    data = df[df["kode_kota"] == kota]
    ax.plot(data["tanggal"], data["harga"], label=kota)

ax.set_xlabel("Tanggal")
ax.set_ylabel("Harga")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ===============================
# Statistik Ringkas
# ===============================
st.subheader("📊 Statistik Ringkas")

summary = (
    df.groupby("kode_kota")["harga"]
    .agg(["mean", "min", "max"])
    .round(0)
    .reset_index()
)

st.dataframe(summary)
