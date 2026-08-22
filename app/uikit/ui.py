"""
Design system bersama untuk seluruh halaman Streamlit.

Menyediakan: setup halaman + CSS, header hero, stat card, dan selector
(kota & komoditas) yang konsisten di semua halaman.
"""
import streamlit as st

from etl.komoditas import get_catalog_from_db
from app.services.data_service import get_daftar_kota

# ---- Palet brand (chrome) --------------------------------------------------
BRAND = "#0f766e"        # teal-700
BRAND_DARK = "#0b5c55"
INK = "#0b0b0b"
INK_MUTED = "#52514e"

_CSS = """
<style>
:root {
    --brand: #0f766e;
    --brand-dark: #0b5c55;
    --ink: #0b0b0b;
    --ink-muted: #52514e;
    --surface: #ffffff;
    --line: rgba(11,11,11,0.08);
}

/* Sembunyikan chrome bawaan yang ramai */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }

/* Lebar konten & tipografi */
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }
html, body, [class*="css"] {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
h1, h2, h3 { letter-spacing: -0.01em; color: var(--ink); }

/* Hero header */
.app-hero {
    background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);
    color: #ffffff;
    padding: 1.6rem 1.8rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px -12px rgba(15,118,110,0.5);
}
.app-hero h1 {
    color: #ffffff; margin: 0; font-size: 1.7rem; font-weight: 700;
}
.app-hero p {
    color: rgba(255,255,255,0.85); margin: 0.35rem 0 0; font-size: 0.98rem;
}

/* Stat cards (KPI) */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr)); gap: 0.9rem; margin: 0.5rem 0 1.2rem; }
.stat-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    box-shadow: 0 1px 2px rgba(11,11,11,0.04);
}
.stat-card .label { color: var(--ink-muted); font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.03em; }
.stat-card .value { color: var(--ink); font-size: 1.55rem; font-weight: 700; margin-top: 0.25rem; }
.stat-card .sub { color: var(--ink-muted); font-size: 0.82rem; margin-top: 0.15rem; }
.stat-card.accent { border-top: 3px solid var(--brand); }

/* Restyle st.metric jadi kartu */
div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    box-shadow: 0 1px 2px rgba(11,11,11,0.04);
}
div[data-testid="stMetricLabel"] p { color: var(--ink-muted); font-weight: 500; }

/* Tombol */
.stButton > button, .stDownloadButton > button {
    border-radius: 10px; font-weight: 600; border: 1px solid transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] { border-right: 1px solid var(--line); }
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* Badge sederhana */
.badge { display:inline-block; padding: 0.2rem 0.6rem; border-radius: 999px;
    background: rgba(15,118,110,0.1); color: var(--brand-dark);
    font-size: 0.78rem; font-weight: 600; }
</style>
"""


def setup_page(title: str, icon: str = "📊", layout: str = "wide"):
    """Panggil sekali di awal setiap halaman."""
    st.set_page_config(page_title=title, page_icon=icon, layout=layout)
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="app-hero">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_rupiah(value) -> str:
    try:
        return "Rp " + f"{int(round(float(value))):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "—"


def stat_cards(cards: list[dict]):
    """
    cards: list of {"label","value","sub"(opsional),"accent"(bool opsional)}
    """
    html = ['<div class="stat-grid">']
    for c in cards:
        cls = "stat-card accent" if c.get("accent") else "stat-card"
        sub = f'<div class="sub">{c["sub"]}</div>' if c.get("sub") else ""
        html.append(
            f'<div class="{cls}"><div class="label">{c["label"]}</div>'
            f'<div class="value">{c["value"]}</div>{sub}</div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


# ---- Selector bersama -------------------------------------------------------

@st.cache_data(ttl=120)
def _kota():
    return get_daftar_kota()


@st.cache_data(ttl=120)
def _komoditas():
    return get_catalog_from_db()  # [(id, nama), ...]


def pilih_kota(label: str = "Kota", key: str | None = None):
    opsi = _kota()
    if not opsi:
        st.warning("Belum ada data. Ambil data dulu di halaman **🔄 Fetch Data**.")
        st.stop()
    return st.selectbox(label, opsi, key=key)


def pilih_kota_multi(label: str = "Pilih Kota", default_n: int = 2, key: str | None = None):
    opsi = _kota()
    if not opsi:
        st.warning("Belum ada data. Ambil data dulu di halaman **🔄 Fetch Data**.")
        st.stop()
    default = opsi[:default_n]
    return st.multiselect(label, opsi, default=default, key=key)


def pilih_komoditas(label: str = "Komoditas", key: str | None = None):
    """Return (komoditas_id, komoditas_nama)."""
    items = _komoditas()
    if not items:
        st.warning("Belum ada data. Ambil data dulu di halaman **🔄 Fetch Data**.")
        st.stop()
    opsi = {nama: kid for kid, nama in items}
    nama = st.selectbox(label, list(opsi.keys()), key=key)
    return opsi[nama], nama
