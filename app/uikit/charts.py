"""
Pembuat chart Plotly dengan gaya konsisten.

Palet kategorikal memakai palet tervalidasi (CVD-safe) dari skill dataviz:
urutan tetap blue → orange → aqua → yellow → magenta → green → violet → red.
"""
import plotly.graph_objects as go

# Palet kategorikal tervalidasi (light mode)
CATEGORICAL = [
    "#2a78d6",  # blue
    "#eb6834",  # orange
    "#1baf7a",  # aqua
    "#eda100",  # yellow
    "#e87ba4",  # magenta
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
]

BLUE = "#2a78d6"
AQUA = "#1baf7a"
ORANGE = "#eb6834"

# Chart chrome / ink
SURFACE = "#ffffff"
INK = "#0b0b0b"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
MUTED = "#898781"

_FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def _style(fig: go.Figure, height: int = 380, rupiah: bool = True) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=8, r=8, t=16, b=8),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family=_FONT, size=13, color=INK),
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, bgcolor="rgba(0,0,0,0)",
            font=dict(color=INK),
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor=AXIS, tickcolor=AXIS, color=MUTED)
    fig.update_yaxes(
        gridcolor=GRID, zeroline=False, linecolor="rgba(0,0,0,0)",
        color=MUTED, tickprefix="Rp " if rupiah else None, separatethousands=True,
    )
    return fig


def line_price(df, x, y, name="Harga", height=380):
    """Line chart satu seri (harga harian)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y], mode="lines", name=name,
        line=dict(color=BLUE, width=2),
        hovertemplate="%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra></extra>",
    ))
    return _style(fig, height)


def monthly_band(df, height=400):
    """Trend bulanan: rata-rata + pita rentang (terendah–tertinggi)."""
    fig = go.Figure()
    # Pita rentang
    fig.add_trace(go.Scatter(
        x=df.index, y=df["harga_tertinggi"], mode="lines",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df["harga_terendah"], mode="lines",
        line=dict(width=0), fill="tonexty",
        fillcolor="rgba(42,120,214,0.12)", name="Rentang (min–max)",
        hoverinfo="skip",
    ))
    # Rata-rata
    fig.add_trace(go.Scatter(
        x=df.index, y=df["harga_ratarata"], mode="lines+markers",
        line=dict(color=BLUE, width=2.5), marker=dict(size=6),
        name="Rata-rata",
        hovertemplate="%{x|%b %Y}<br>Rp %{y:,.0f}<extra></extra>",
    ))
    return _style(fig, height)


def compare_lines(df, cities, height=440):
    """Beberapa kota dalam satu chart (palet kategorikal, warna per kota)."""
    fig = go.Figure()
    for i, kota in enumerate(cities):
        data = df[df["kode_kota"] == kota]
        fig.add_trace(go.Scatter(
            x=data["tanggal"], y=data["harga"], mode="lines", name=kota,
            line=dict(color=CATEGORICAL[i % len(CATEGORICAL)], width=2),
            hovertemplate=f"<b>{kota}</b><br>%{{x|%d %b %Y}}<br>Rp %{{y:,.0f}}<extra></extra>",
        ))
    return _style(fig, height)


def forecast_chart(train, test, forecast, height=430):
    """Train (blue) + Aktual (aqua) + Forecast (orange)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=train.index, y=train.values, mode="lines", name="Train",
        line=dict(color=BLUE, width=2),
        hovertemplate="%{x|%b %Y}<br>%{y:,.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=test.index, y=test.values, mode="lines+markers", name="Aktual",
        line=dict(color=AQUA, width=2), marker=dict(size=6),
        hovertemplate="%{x|%b %Y}<br>%{y:,.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index, y=forecast.values, mode="lines+markers", name="Forecast",
        line=dict(color=ORANGE, width=2.5, dash="dash"), marker=dict(size=6),
        hovertemplate="%{x|%b %Y}<br>%{y:,.2f}<extra></extra>",
    ))
    return _style(fig, height)
