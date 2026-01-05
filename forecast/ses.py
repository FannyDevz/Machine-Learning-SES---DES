from statsmodels.tsa.holtwinters import SimpleExpSmoothing


def fit_ses(train_series, forecast_steps: int):
    model = SimpleExpSmoothing(
        train_series,
        initialization_method="estimated"
    )

    fit = model.fit()

    forecast = fit.forecast(forecast_steps)

    return fit, forecast
