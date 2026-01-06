import streamlit as st
from services.data_service import get_daftar_kota

def sidebar_filters():
    kota = st.sidebar.selectbox(
        "Pilih Kota",
        get_daftar_kota()
    )

    tipe = st.sidebar.radio(
        "Tipe Beras",
        ["medium", "premium"]
    )

    return kota, tipe
