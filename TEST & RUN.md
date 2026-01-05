# TESTING

## Test config/settings.py

```bash
    python -c "from config.settings import debug; debug()"
```

## Test database/connection.py

```bash
    python -c "from database.connection import get_engine; engine = get_engine(); print(engine)"
```

## Test database/queries.py

```bash
python -c "from database.queries import get_harga_harian; df = get_harga_harian('2024-01-01', '2024-12-31'); print(df)"

```

## Test etl/extract.py

```bash
python -c "from etl.extract import extract_range; df = extract_range('2026-01-04', '2026-01-04'); print(df.head()); print(len(df)) "
```

```bash
python -c "from database.queries import get_harga_harian; df = get_harga_harian('2026-01-01', '2026-01-04'); print(df.head()); print(df['tipe'].value_counts());"
```

# RUNNING

## env

```
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=data_beras
DB_PORT=3308

# App
APP_ENV=development

```

## Run database/migration.py

```bash
python -m database.migrations
```

## CHANGE DATE IN run_etl.py

```py
df_raw = extract_range(
        start_date="2024-01-01",
        end_date="2025-12-31"
    )
```

## Run run_etl.py

```bash
python -m etl.run_etl
```

## Run export_csv.py

```bash
python -c "from export.export_csv import export_harian_to_csv; export_harian_to_csv('2026-01-01','2026-01-31')"
```

## Export CSV

```bash
python -c "from export.export_csv import export_monthly_to_csv; export_monthly_to_csv(2026)"

```
