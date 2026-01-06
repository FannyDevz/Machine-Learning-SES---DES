import pandas as pd

def generate_future_dates(last_date, n_periods):
    return pd.date_range(
        start=last_date + pd.offsets.MonthBegin(1),
        periods=n_periods,
        freq="MS"
    )
