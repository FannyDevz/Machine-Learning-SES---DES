def daily_stats(df):
    return {
        "min": df["harga"].min(),
        "max": df["harga"].max(),
        "mean": df["harga"].mean(),
        "median": df["harga"].median(),
        "std": df["harga"].std()
    }
