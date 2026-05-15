# Description: Short example for Time Series Analysis in Earth Science with EarthPy.



from data_io import read_csv
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import earthpy as et
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)



# Download example data
data = et.data.get_data("cold-springs-fire")

# Define file path for the raster time series
lst_path = os.path.join(data, "outputs", "modis_lst_example.csv")

# Load the dataset
df = read_csv(lst_path)

# Convert the `date` column to a datetime object
df['date'] = pd.to_datetime(df['date'])

# Display the first few rows
logger.info(df.head())

plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['temperature'], label="Land Surface Temperature")
plt.title("Land Surface Temperature Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.savefig("land_surface_temperature_over_time.png")
plt.show()


# Set the date column as the index for decomposition
df.set_index('date', inplace=True)

# Perform seasonal decomposition
result = seasonal_decompose(df['temperature'], model='additive', period=365)

# Plot the decomposition
result.plot()
plt.savefig("seasonal_decomposition.png")
plt.show()

# Calculate rolling mean and standard deviation
rolling_mean = df['temperature'].rolling(window=30).mean()
rolling_std = df['temperature'].rolling(window=30).std()

# Identify anomalies
anomalies = df[(df['temperature'] > rolling_mean + 2 * rolling_std) |
               (df['temperature'] < rolling_mean - 2 * rolling_std)]

# Plot anomalies
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['temperature'], label="Temperature")
plt.scatter(anomalies.index, anomalies['temperature'], color='red', label="Anomalies")
plt.title("Temperature Anomalies")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.savefig("temperature_anomalies.png")
plt.show()


# Fit an ARIMA model
model = ARIMA(df['temperature'], order=(5, 1, 0))
fit = model.fit()

# Forecast future temperatures
forecast = fit.forecast(steps=365)

# Plot the forecast
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['temperature'], label="Historical Temperature")
plt.plot(pd.date_range(df.index[-1], periods=365, freq='D'), forecast, label="Forecast")
plt.title("Temperature Forecast")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.savefig("temperature_forecast.png")
plt.show()
