import matplotlib.pyplot as plt

def plot_daily_price(df, title="Harga Harian"):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df["harga"], marker="o")
    ax.set_title(title)
    ax.set_ylabel("Harga")
    ax.grid(True)
    return fig
