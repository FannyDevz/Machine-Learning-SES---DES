from forecast.ses import fit_ses
from forecast.des import fit_des
from forecast.evaluate import mae, rmse,mape


def auto_select_model(train, test, metric="mape"):
    """
    metric: 'mape' | 'rmse' | 'mae'
    """

    # SES
    _, ses_forecast = fit_ses(train, len(test))
    ses_mae = mae(test, ses_forecast)
    ses_mape = mape(test, ses_forecast)
    ses_rmse = rmse(test, ses_forecast)

    # DES
    _, des_forecast = fit_des(train, len(test))
    des_mae = mae(test, des_forecast)
    des_mape = mape(test, des_forecast)
    des_rmse = rmse(test, des_forecast)

    # Pastikan ses_score dan des_score selalu terisi apapun metriknya
    if metric == "mae":
        ses_score, des_score = ses_mae, des_mae
    elif metric == "rmse":
        ses_score, des_score = ses_rmse, des_rmse
    else:
        ses_score, des_score = ses_mape, des_mape

    if ses_score <= des_score:
        return {
            "model": "SES",
            "forecast": ses_forecast,
            "mape": ses_mape,
            "mae": ses_mae,
            "rmse": ses_rmse
        }
    else:
        return {
            "model": "DES",
            "forecast": des_forecast,
            "mape": des_mape,
            "mae": des_mae,
            "rmse": des_rmse
        }
