# Beras Price Analysis Project

## Deskripsi

Project ini bertujuan untuk mengumpulkan, menyimpan, menganalisis, dan
memvisualisasikan data harga beras berdasarkan kota dan waktu (harian
dan bulanan).
Project ini dirancang modular dan scalable untuk kebutuhan analisis
data, statistik, serta pembuatan dashboard menggunakan Streamlit.

## Teknologi yang Digunakan

- Python 3.9+
- MySQL
- Pandas
- NumPy
- Statsmodels
- Streamlit

## Struktur Project (Ringkas)

- database : koneksi, migrasi, dan query database
- etl : proses fetch, transform, dan load data
- analysis : analisis data dan time series
- app : aplikasi Streamlit
- config : konfigurasi environment
- utils : helper functions

## Instalasi

1. Clone Repository

```bash
    git clone <repository-url>
    cd beras-project
```

2. Buat Virtual Environment

```bash
    python -m venv .venv
```

Aktifkan virtual environment:

Linux / Mac:

```bash
    source .venv/bin/activate
```

Windows:

```bash
    .venv\Scripts\activate
```

3. Install Dependencies

```bash
    pip install -r requirements.txt
```

4. Konfigurasi Environment

Buat file .env di root project:

```py
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=root
    DB_NAME=beras
    DB_PORT=8889
```

5. Jalankan Migrasi Database

```bash
    python -m database.migrations
```

6. Jalankan Aplikasi Streamlit

```bash
    streamlit run app/main.py
```

## Catatan

- File .env tidak boleh di-commit ke repository
- Pastikan MySQL sudah berjalan sebelum menjalankan migrasi
- Struktur project dirancang agar mudah dikembangkan untuk analisis
  lanjutan dan forecasting

### Author

Data Analysis Project
