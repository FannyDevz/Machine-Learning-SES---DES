from statsmodels.tsa.holtwinters import Holt


def fit_des(train_series, forecast_steps: int):
    model = Holt(
        train_series,
        initialization_method="estimated"
    )

    fit = model.fit()

    forecast = fit.forecast(forecast_steps)

    return fit, forecast
