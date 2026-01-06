def monthly_change(df):
    df = df.copy()
    df["mom_change"] = df["harga_ratarata"].diff()
    df["mom_pct"] = df["harga_ratarata"].pct_change() * 100
    return df
