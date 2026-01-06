from datetime import datetime, timedelta
from etl.extract import extract_daily

def main():
    
    start_date = "2025-01-01"
    end_date = "2026-01-01"
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    current = start
    while current <= end:
        tanggal = current.strftime("%Y-%m-%d")
        print(f"Fetching tanggal: {tanggal}")
        extract_daily(tanggal)
        print(f"Selesai tanggal: {tanggal}")
        current += timedelta(days=1)
    return


if __name__ == "__main__":
    main()
