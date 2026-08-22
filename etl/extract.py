import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Iterable
from utils.logger import logger
from etl.komoditas import get_catalog

BASE_URL = "https://siskaperbapo.jatimprov.go.id/home2/getDataMap/"


def fetch_harga_by_date(
    tanggal: str,
    komoditas_id: int
) -> List[dict]:
    """
    Fetch harga satu komoditas per tanggal.
    Nama komoditas diambil langsung dari respons API.
    Return list of rows.
    """
    params = {
        "tanggal": tanggal,
        "komoditas": komoditas_id
    }

    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()

    json_data = resp.json()
    data = json_data.get("data", {})
    nama_komoditas = (json_data.get("komoditas_nama") or "").strip() \
        or get_catalog().get(int(komoditas_id), f"Komoditas {komoditas_id}")

    rows = []

    for _, item in data.items():
        harga = item.get("hrg", 0)

        # Skip harga tidak valid
        if not harga or harga <= 0:
            continue

        rows.append({
            "kode_kota": item.get("code"),
            "nama_kota": item.get("nama"),
            "komoditas_id": int(komoditas_id),
            "komoditas_nama": nama_komoditas,
            "harga": int(harga),
            "tanggal": tanggal
        })
    return rows


def _normalize_komoditas(komoditas_ids: Iterable[int] | None) -> List[int]:
    if not komoditas_ids:
        # default: beras premium + medium (perilaku lama)
        return [2, 4]
    return [int(k) for k in komoditas_ids]


def extract_range(
    start_date: str,
    end_date: str,
    komoditas_ids: Iterable[int] | None = None
) -> pd.DataFrame:
    """
    Extract data untuk range tanggal (YYYY-MM-DD) dan daftar komoditas.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    komoditas_ids = _normalize_komoditas(komoditas_ids)

    all_rows = []

    current = start
    while current <= end:
        tanggal = current.strftime("%Y-%m-%d")
        for kid in komoditas_ids:
            try:
                rows = fetch_harga_by_date(tanggal, kid)
                all_rows.extend(rows)
                logger.info(
                    f"Extract sukses | tanggal={tanggal} | komoditas={kid} | rows={len(rows)}"
                )
            except Exception as e:
                logger.error(
                    f"Extract gagal | tanggal={tanggal} | komoditas={kid} | error={str(e)}"
                )
        current += timedelta(days=1)

    return pd.DataFrame(all_rows)


def extract_daily(
    daily: str,
    komoditas_ids: Iterable[int] | None = None
) -> pd.DataFrame:
    """
    Extract data satu tanggal (YYYY-MM-DD) untuk daftar komoditas.
    """
    daily = datetime.strptime(daily, "%Y-%m-%d")
    komoditas_ids = _normalize_komoditas(komoditas_ids)

    all_rows = []

    tanggal = daily.strftime("%Y-%m-%d")
    for kid in komoditas_ids:
        try:
            rows = fetch_harga_by_date(tanggal, kid)
            all_rows.extend(rows)
            logger.info(
                f"Extract sukses | tanggal={tanggal} | komoditas={kid} | rows={len(rows)}"
            )
        except Exception as e:
            logger.error(
                f"Extract gagal | tanggal={tanggal} | komoditas={kid} | error={str(e)}"
            )

    return pd.DataFrame(all_rows)
