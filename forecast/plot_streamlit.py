import pandas as pd
import matplotlib.pyplot as plt

def plot_forecast(train, test, forecast, title="Forecast"):
    # 🔑 PASTIKAN forecast punya index
    if not isinstance(forecast, pd.Series):
        forecast = pd.Series(forecast, index=test.index)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(train.index, train.values, label="Train")
    ax.plot(test.index, test.values, label="Actual")
    ax.plot(forecast.index, forecast.values, label="Forecast")

    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    return fig
