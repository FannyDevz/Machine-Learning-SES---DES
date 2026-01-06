import pandas as pd

def minmax_scale(series: pd.Series):
    min_val = series.min()
    max_val = series.max()

    scaled = (series - min_val) / (max_val - min_val)

    return scaled, min_val, max_val


def minmax_inverse(scaled: pd.Series, min_val, max_val):
    return scaled * (max_val - min_val) + min_val
