def detect_spike(df, threshold_pct=5):
    df = df.copy()
    df["pct_change"] = df["harga"].pct_change() * 100
    return df[df["pct_change"].abs() >= threshold_pct]
