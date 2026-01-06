def daily_change(df):
    df = df.copy()
    df["delta"] = df["harga"].diff()
    df["pct_change"] = df["harga"].pct_change() * 100
    return df
