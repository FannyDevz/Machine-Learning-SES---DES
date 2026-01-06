import matplotlib.pyplot as plt


def plot_forecast(train, test, forecast, title="Forecast"):
    plt.figure(figsize=(10, 5))

    train.plot(label="Train")
    test.plot(label="Actual", marker="o")
    forecast.plot(label="Forecast", marker="x")

    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

