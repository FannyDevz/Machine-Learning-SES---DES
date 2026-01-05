import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List
from utils.logger import logger

BASE_URL = "https://siskaperbapo.jatimprov.go.id/home2/getDataMap/"

KOMODITAS = {
    "premium": 2,
    "medium": 4
}


def fetch_harga_by_date(
    tanggal: str,
    tipe: str
) -> List[dict]:
    """
    Fetch harga beras per tanggal & tipe (premium / medium)
    Return list of rows
    """
    params = {
        "tanggal": tanggal,
        "komoditas": KOMODITAS[tipe]
    }

    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()

    json_data = resp.json()
    data = json_data.get("data", {})

    rows = []

    for _, item in data.items():
        harga = item.get("hrg", 0)

        # Skip harga tidak valid
        if not harga or harga <= 0:
            continue

        rows.append({
            "kode_kota": item.get("code"),
            "nama_kota": item.get("nama"),
            "tipe": tipe,
            "harga": int(harga),
            "tanggal": tanggal
        })
    return rows


def extract_range(
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Extract data untuk range tanggal (YYYY-MM-DD)
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_rows = []

    current = start
    while current <= end:
        tanggal = current.strftime("%Y-%m-%d")
        for tipe in KOMODITAS.keys():
            try:
                rows = fetch_harga_by_date(tanggal, tipe)
                all_rows.extend(rows)
                logger.info(
                    f"Extract sukses | tanggal={tanggal} | rows={len(rows)}"
                )
            except Exception as e:
                logger.error(
                    f"Extract gagal | tanggal={tanggal} | error={str(e)}"
                )
        current += timedelta(days=1)

    return pd.DataFrame(all_rows)


def extract_daily(
    daily: str,
) -> pd.DataFrame:
    """
    Extract data untuk range tanggal (YYYY-MM-DD)
    """
    daily = datetime.strptime(daily, "%Y-%m-%d")

    all_rows = []

    tanggal = daily.strftime("%Y-%m-%d")
    for tipe in KOMODITAS.keys():
        try:
            rows = fetch_harga_by_date(tanggal, tipe)
            all_rows.extend(rows)
            logger.info(
                f"Extract sukses | tanggal={tanggal} | rows={len(rows)}"
            )
        except Exception as e:
            logger.error(
                f"Extract gagal | tanggal={tanggal} | error={str(e)}"
            )

    return pd.DataFrame(all_rows)
