import logging
import os

import earthpy as et
import matplotlib.pyplot as plt
import pandas as pd
from data_io import read_csv
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose


def download_example_data() -> None:
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    data = et.data.get_data("cold-springs-fire")
    lst_path = os.path.join(data, "outputs", "modis_lst_example.csv")
    df = read_csv(lst_path)
    df["date"] = pd.to_datetime(df["date"])
    logger.info(df.head())
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["temperature"], label="Land Surface Temperature")
    plt.title("Land Surface Temperature Over Time")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.savefig("land_surface_temperature_over_time.png")
    plt.show()
    df.set_index("date", inplace=True)
    result = seasonal_decompose(df["temperature"], model="additive", period=365)
    result.plot()
    plt.savefig("seasonal_decomposition.png")
    plt.show()
    rolling_mean = df["temperature"].rolling(window=30).mean()
    rolling_std = df["temperature"].rolling(window=30).std()
    df[
        (df["temperature"] > rolling_mean + 2 * rolling_std)
        | (df["temperature"] < rolling_mean - 2 * rolling_std)
    ]


def plot_anomalies() -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["temperature"], label="Temperature")
    plt.scatter(anomalies.index, anomalies["temperature"], color="red", label="Anomalies")
    plt.title("Temperature Anomalies")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.savefig("temperature_anomalies.png")
    plt.show()
    model = ARIMA(df["temperature"], order=(5, 1, 0))
    fit = model.fit()
    fit.forecast(steps=365)


def plot_the_forecast() -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["temperature"], label="Historical Temperature")
    plt.plot(pd.date_range(df.index[-1], periods=365, freq="D"), forecast, label="Forecast")
    plt.title("Temperature Forecast")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.savefig("temperature_forecast.png")
    plt.show()


def main() -> None:
    download_example_data()
    plot_anomalies()
    plot_the_forecast()


if __name__ == "__main__":
    main()
