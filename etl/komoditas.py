"""
Katalog komoditas SISKAPERBAPO.

Sumber data mendukung banyak komoditas (bukan hanya beras). Setiap komoditas
diidentifikasi oleh `komoditas_id` (parameter `komoditas` pada API).

- DEFAULT_CATALOG dipakai untuk daftar pilihan di UI Fetch (tanpa perlu jaringan).
- refresh_catalog_from_api() bisa dipakai untuk memuat ulang nama komoditas
  langsung dari API bila diperlukan.
- get_catalog_from_db() mengambil komoditas yang SUDAH ada datanya di database
  (dipakai halaman analitik/forecast agar hanya menampilkan yang tersedia).
"""

import requests
from sqlalchemy import text

from database.connection import get_engine
from config.settings import DB_NAME
from utils.logger import logger

BASE_URL = "https://siskaperbapo.jatimprov.go.id/home2/getDataMap/"

# id -> nama komoditas (fallback statis untuk pilihan di UI)
DEFAULT_CATALOG = {
    2: "Beras Premium",
    3: "Beras Mentik",
    4: "Beras Medium",
    7: "Gula Kristal Putih",
    9: "Minyak Goreng Bimoli Botol",
    10: "Minyak Goreng Curah",
    12: "Daging Sapi Paha Belakang",
    13: "Daging Ayam Ras",
    14: "Daging Ayam Kampung",
    16: "Telur Ayam Ras",
    17: "Telur Ayam Kampung",
    20: "Susu Kental Manis Bendera",
    21: "Susu Kental Manis Indomilk",
    23: "Susu Bubuk Bendera",
    24: "Susu Bubuk Indomilk",
    25: "Jagung Pipilan Kering",
    27: "Garam Beryodium Bata",
    28: "Garam Beryodium Halus",
    30: "Tepung Terigu",
    32: "Kacang Kedelai Impor",
    33: "Kacang Kedelai Lokal",
    35: "Indomie Rasa Kari Ayam",
    37: "Cabe Merah Keriting",
    38: "Cabe Merah Besar",
    39: "Bawang Merah",
    40: "Ikan Asin Teri",
    41: "Kacang Hijau",
    42: "Kacang Tanah",
    43: "Ketela Pohon",
    44: "Kol/Kubis",
    45: "Kentang",
    46: "Tomat",
    47: "Wortel",
    48: "Buncis",
    49: "Bawang Putih",
    50: "Cabe Rawit Merah",
    54: "Semen Gresik",
    55: "Semen Tiga Roda",
    58: "Ikan Bandeng",
    59: "Ikan Kembung",
    60: "Ikan Tongkol",
    61: "Ikan Tuna",
    62: "Ikan Cakalang",
    67: "Kayu Balok Meranti",
    68: "Papan Meranti",
    69: "Triplek 6mm",
}


def get_catalog() -> dict[int, str]:
    """Katalog komoditas untuk dipilih di UI (id -> nama)."""
    return dict(DEFAULT_CATALOG)


def komoditas_nama(komoditas_id: int) -> str:
    return DEFAULT_CATALOG.get(int(komoditas_id), f"Komoditas {komoditas_id}")


def refresh_catalog_from_api(tanggal: str, id_range=range(1, 71)) -> dict[int, str]:
    """
    Muat ulang katalog dari API pada tanggal tertentu.
    Hanya mengembalikan komoditas yang punya nama valid.
    """
    catalog: dict[int, str] = {}
    for k in id_range:
        try:
            resp = requests.get(
                BASE_URL, params={"tanggal": tanggal, "komoditas": k}, timeout=15
            )
            resp.raise_for_status()
            nama = (resp.json().get("komoditas_nama") or "").strip()
            if nama and nama != "-":
                catalog[k] = nama
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Refresh katalog gagal | komoditas={k} | error={e}")
    return catalog


def get_catalog_from_db() -> list[tuple[int, str]]:
    """
    Daftar (komoditas_id, komoditas_nama) yang sudah punya data harian di DB.
    Dipakai halaman analitik/forecast agar hanya menampilkan komoditas tersedia.
    """
    engine = get_engine(DB_NAME)
    query = text("""
        SELECT DISTINCT komoditas_id, komoditas_nama
        FROM history_data_komoditas
        ORDER BY komoditas_nama
    """)
    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()
    return [(int(r[0]), r[1]) for r in rows]
