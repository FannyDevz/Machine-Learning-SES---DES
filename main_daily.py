
def main():
    
    # from datetime import datetime, timedelta
    # from etl.extract import extract_daily
    # start_date = "2025-01-01"
    # end_date = "2026-01-01"
    # start = datetime.strptime(start_date, "%Y-%m-%d")
    # end = datetime.strptime(end_date, "%Y-%m-%d")

    # current = start
    # while current <= end:
    #     tanggal = current.strftime("%Y-%m-%d")
    #     print(f"Fetching tanggal: {tanggal}")
    #     extract_daily(tanggal)
    #     print(f"Selesai tanggal: {tanggal}")
    #     current += timedelta(days=1)
    # return
    from forecast.dataset import load_monthly_series
    from forecast.split import train_test_split_ts
    from forecast.ses import fit_ses
    from forecast.des import fit_des
    from forecast.evaluate import mae, mape
    from forecast.plot import plot_forecast

    series = load_monthly_series("surabayakota", "premium")

    train, test = train_test_split_ts(series, test_size=1)

    # SES
    _, ses_forecast = fit_ses(train, len(test))

    # DES
    _, des_forecast = fit_des(train, len(test))

    print("SES MAE:", mae(test, ses_forecast))
    print("DES MAE:", mae(test, des_forecast))

    plot_forecast(train, test, ses_forecast, "SES Forecast")
    plot_forecast(train, test, des_forecast, "DES Forecast")



if __name__ == "__main__":
    main()
