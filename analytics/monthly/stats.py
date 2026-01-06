def monthly_summary(df):
    return {
        "avg": df["harga_ratarata"].mean(),
        "max": df["harga_tertinggi"].max(),
        "min": df["harga_terendah"].min(),
        "bulan_termahal": df["harga_tertinggi"].idxmax(),
        "bulan_termurah": df["harga_terendah"].idxmin()
    }
