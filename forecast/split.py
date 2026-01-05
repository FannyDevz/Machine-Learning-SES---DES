def train_test_split_ts(
    series,
    test_size: int = 3
):
    if len(series) <= test_size:
        raise ValueError("Data terlalu sedikit untuk split")

    train = series.iloc[:-test_size]
    test = series.iloc[-test_size:]

    return train, test
