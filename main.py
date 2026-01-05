from database.migrations import run_migrations
from etl.run_etl import run as fetch_harga
from export.export_csv import export_harian_to_csv, export_monthly_to_csv
from etl.aggregate import aggregate_monthly

def menu():
    print("\n=== MENU ===")
    print("1. Running Migration")
    print("2. Fetch Harga")
    print("3. Transform Data Ke Bulanan")
    print("4. Export Data Harian ke CSV")
    print("5. Export Data Bulanan ke CSV")
    print("0. Keluar")
    return input("Pilih menu: ")


def input_range_tanggal():
    print("\nFormat tanggal: YYYY-MM-DD")
    start_date = input("Masukkan start date (kosongkan = hari ini): ").strip()
    end_date = input("Masukkan end date   (kosongkan = hari ini): ").strip()

    # Jika kosong, jadikan None agar pakai default
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None

    return start_date, end_date

def input_range_tahun():
    print("\nFormat tahun: YYYY")
    start_year = input("Masukkan start year (kosongkan = tahun ini): ").strip()
    end_year = input("Masukkan end year   (kosongkan = tahun ini): ").strip()

    # Jika kosong, jadikan None agar pakai default
    start_year = start_year if start_year else None
    end_year = end_year if end_year else None

    return start_year, end_year

def input_tahun():
    print("\nFormat tahun: YYYY")
    tahun = input("Masukkan tahun (kosongkan = tahun ini): ").strip()
    tahun = tahun if tahun else None
    return tahun

def main():
    while True:
        pilihan = menu()
        if pilihan == "1":
            run_migrations()
        elif pilihan == "2":
            start_date, end_date = input_range_tanggal()
            fetch_harga(start_date=start_date, end_date=end_date)
        elif pilihan == "3":
            start_year, end_year = input_range_tahun()
            aggregate_monthly(start_year=start_year, end_year=end_year)
        elif pilihan == "4":
            start_date, end_date = input_range_tanggal()
            export_harian_to_csv(start_date=start_date, end_date=end_date)
        elif pilihan == "5":
            tahun = input_tahun()
            export_monthly_to_csv(tahun)
        elif pilihan == "0":
            print("Keluar program.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
