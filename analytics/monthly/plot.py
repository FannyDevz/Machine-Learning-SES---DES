import matplotlib.pyplot as plt

def plot_monthly_trend(df, title="Trend Harga Bulanan"):
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(df.index, df["harga_ratarata"], marker="o", label="Rata-rata")
    ax.fill_between(
        df.index,
        df["harga_terendah"],
        df["harga_tertinggi"],
        alpha=0.2,
        label="Rentang Harga"
    )

    ax.set_title(title)
    ax.set_ylabel("Harga")
    ax.legend()
    ax.grid(True)

    return fig
