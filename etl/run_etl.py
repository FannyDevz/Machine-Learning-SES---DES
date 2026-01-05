from etl.extract import extract_range,extract_daily
from etl.transform import transform_data
from etl.load import load_to_db
from utils.logger import logger
from utils.date import today

def run_daily(daily=None):
    
    if not daily:
        daily = today()

    df_raw = extract_daily(daily)

    df_clean = transform_data(df_raw)
    load_to_db(df_clean)
    
    logger.info(
        f"ETL SELESAI | total_rows={len(df_clean)}"
    )

def run(start_date=None, end_date=None):
    
    if not start_date:
        start_date = today()
    if not end_date:
        end_date = today()

    df_raw = extract_range(
        start_date=start_date,
        end_date=end_date
    )

    df_clean = transform_data(df_raw)
    load_to_db(df_clean)
    
    logger.info(
        f"ETL SELESAI | total_rows={len(df_clean)}"
    )

if __name__ == "__main__":
    run()
