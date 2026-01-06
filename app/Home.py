import streamlit as st

st.set_page_config(
    page_title="Analisis & Forecast Harga Beras",
    layout="wide"
)

st.title("📊 Analisis & Forecast Harga Beras")

st.markdown("""
Aplikasi ini digunakan untuk:
- Analisis harga beras harian & bulanan
- Agregasi data per kota
- Prediksi harga menggunakan metode **Exponential Smoothing**
""")

st.info("Gunakan menu di sidebar untuk navigasi")
