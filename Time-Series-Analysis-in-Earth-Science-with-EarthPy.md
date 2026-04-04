# Time Series Analysis in Earth Science with EarthPy

## Introduction

Time series analysis plays a vital role in Earth science, helping researchers analyze phenomena like temperature changes, rainfall patterns, glacier melting, and more. By studying temporal patterns in Earth science data, we can better understand environmental changes, predict future trends, and guide policy decisions.

**EarthPy** is a Python package designed for working with spatial data in Earth science. It provides functionalities for handling raster and vector data, analyzing temporal patterns, and visualizing environmental changes. EarthPy integrates well with other libraries such as Pandas, Matplotlib, and NumPy, making it a versatile tool for time series analysis.

⚠️ **Note**: This article demonstrates concepts using standard Python libraries. EarthPy requires specific geospatial dependencies. Install with:
```bash
pip install earthpy
```

## Case Study: Analyzing Land Surface Temperature Trends

In this example, we'll analyze a time series of land surface temperature (LST) data. This type of analysis can provide insights into climate trends, urban heat islands, and agricultural conditions.

### Step 1: Importing Required Libraries

```python
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
```

### Step 2: Loading and Preprocessing Data

For this example, we'll use LST data available through EarthPy's example datasets. You can also use your own raster data for similar analysis.

```python
# Download example data
data = et.data.get_data("cold-springs-fire")

# Define file path for the raster time series
import os
lst_path = os.path.join(data, "outputs", "modis_lst_example.csv")

# Load the dataset
df = pd.read_csv(lst_path)

# Convert the `date` column to a datetime object
df['date'] = pd.to_datetime(df['date'])

# Display the first few rows
print(df.head())
```

The dataset contains columns like `date`, `temperature`, and `location`, representing time series data of land surface temperature.

### Step 3: Exploring the Data

Let's plot the raw time series to get a sense of the data.

```python
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['temperature'], label="Land Surface Temperature")
plt.title("Land Surface Temperature Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.savefig("land_surface_temperature_over_time.png")
plt.show()
```

This visualization provides an overview of temperature fluctuations over time.

### Step 4: Analyzing Seasonal Trends

Many Earth science phenomena exhibit seasonal trends. We'll decompose the time series to separate seasonal, trend, and residual components.

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Set the date column as the index for decomposition
df.set_index('date', inplace=True)

# Perform seasonal decomposition
result = seasonal_decompose(df['temperature'], model='additive', period=365)

# Plot the decomposition
result.plot()
plt.savefig("seasonal_decomposition.png")
plt.show()
```

This decomposition reveals the underlying trend and seasonality of the temperature data.

### Step 5: Detecting Anomalies

Anomaly detection is critical for identifying unusual events such as extreme temperatures or abrupt changes.

```python
# Calculate rolling mean and standard deviation
rolling_mean = df['temperature'].rolling(window=30).mean()
rolling_std = df['temperature'].rolling(window=30).std()

# Identify anomalies
anomalies = df[(df['temperature'] > rolling_mean + 2 * rolling_std) |
               (df['temperature'] < rolling_mean - 2 * rolling_std)]

# Plot anomalies
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['temperature'], label="Temperature")
plt.scatter(anomalies.index, anomalies['temperature'], 
           color='red', label="Anomalies", s=50)
plt.title("Temperature Anomalies")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.savefig("temperature_anomalies.png")
plt.show()
```

By highlighting anomalies, we can investigate potential environmental or climatic drivers behind these events.

### Step 6: Forecasting Future Trends

Finally, forecasting helps predict future temperature trends based on historical data.

```python
from statsmodels.tsa.arima.model import ARIMA

# Fit an ARIMA model
model = ARIMA(df['temperature'], order=(5, 1, 0))
fit = model.fit()

# Forecast future temperatures
forecast = fit.forecast(steps=365)

# Plot the forecast
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['temperature'], label="Historical Temperature")
plt.plot(pd.date_range(df.index[-1], periods=365, freq='D'), 
        forecast, label="Forecast", color='red', linestyle='--')
plt.title("Temperature Forecast")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.savefig("temperature_forecast.png")
plt.show()
```

Forecasting allows us to project trends and prepare for future environmental changes.

## Data Requirements for Production

⚠️ **Note**: The code examples above require actual Earth science data. For production use:

### Land Surface Temperature Data
- **MODIS LST Product**: https://modis.gsfc.nasa.gov/
- **Landsat Thermal**: https://landsat.gsfc.nasa.gov/
- Expected format: CSV with columns `date`, `temperature`, `location`

### Satellite Imagery
- **NASA EarthData**: https://earthdata.nasa.gov/
- **Sentinel Hub**: https://www.sentinel-hub.com/
- **Google Earth Engine**: https://earthengine.google.com/

### Climate Data
- **NOAA Climate Data**: https://www.ncdc.noaa.gov/
- **ERA5 Reanalysis**: https://www.ecmwf.int/
- **PRISM**: https://prism.oregonstate.edu/

## Applications of EarthPy for Time Series

### 1. Climate Change Studies
- Track temperature trends over decades
- Analyze precipitation patterns
- Study glacier retreat

### 2. Agricultural Monitoring
- Monitor crop health with NDVI time series
- Predict growing seasons
- Assess drought impacts

### 3. Urban Heat Island Analysis
- Compare urban vs. rural temperature trends
- Identify heat vulnerability zones
- Plan green infrastructure

### 4. Disaster Monitoring
- Track wildfire progression
- Analyze flood impacts
- Monitor hurricane paths

## Key Features of EarthPy

### Raster Processing
- Load and manipulate satellite imagery
- Calculate vegetation indices (NDVI, EVI)
- Temporal raster stacking

### Plotting Utilities
- Beautiful Earth science visualizations
- Hillshade and elevation plots
- Time series plots

### Integration
- Works seamlessly with pandas, numpy
- Compatible with geopandas for vector data
- Integrates with matplotlib for custom plots

## Advantages of EarthPy

1. **Earth Science Focus**: Built specifically for Earth science workflows
2. **Simplified Raster Operations**: Easy raster stacking and band math
3. **Visualization**: Publication-quality plots out of the box
4. **Educational**: Great for teaching and learning

## Limitations

1. **Specialized**: Primarily for Earth science use cases
2. **Dependencies**: Requires GDAL and other geospatial libraries
3. **Learning Curve**: Geospatial concepts can be challenging
4. **Data Management**: Large raster files require substantial storage

## Comparison with Other Tools

| Tool | Best For | Time Series Support |
|------|----------|-------------------|
| **EarthPy** | Earth science education, raster processing | ✓ Basic |
| **Rasterio** | Production raster processing | ✓ Via pandas |
| **GeoPandas** | Vector data, spatial analysis | ✓ Good |
| **xarray** | Multidimensional arrays, NetCDF | ✓✓ Excellent |
| **Google Earth Engine** | Large-scale cloud processing | ✓✓✓ Enterprise |

## Workflow Example: Complete Analysis Pipeline

```python
import earthpy as et
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# 1. Load data
df = pd.read_csv('lst_data.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# 2. Visualize trends
df['temperature'].plot(figsize=(12, 6), title='LST Over Time')
plt.savefig('lst_trend.png')

# 3. Decompose seasonality
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(df['temperature'], model='additive', period=365)
result.plot()
plt.savefig('decomposition.png')

# 4. Detect anomalies
rolling_mean = df['temperature'].rolling(30).mean()
rolling_std = df['temperature'].rolling(30).std()
anomalies = df[(df['temperature'] > rolling_mean + 2*rolling_std) | 
               (df['temperature'] < rolling_mean - 2*rolling_std)]
print(f"Found {len(anomalies)} anomalies")

# 5. Forecast
model = ARIMA(df['temperature'], order=(5,1,0))
fit = model.fit()
forecast = fit.forecast(steps=180)
print(f"6-month forecast: {forecast.mean():.1f}°C ± {forecast.std():.1f}°C")
```

## Best Practices

1. **Data Quality**: Always validate satellite data for clouds, gaps
2. **Temporal Alignment**: Ensure consistent time intervals
3. **Spatial Consistency**: Use the same geographic extent
4. **Computational Efficiency**: Process large rasters in chunks
5. **Version Control**: Track data versions and processing steps

## Conclusion

Time series techniques work for a variety of tasks in Earth science. Using EarthPy and associated libraries, we explored and visualized LST data, analyzed seasonal patterns, detected anomalies, and forecasted future trends. These techniques provide valuable insights for understanding and responding to Earth's dynamic systems.

By applying similar methods to other Earth science datasets, researchers can uncover trends and make data-driven decisions to address pressing environmental challenges.

## Resources

- **EarthPy Documentation**: https://earthpy.readthedocs.io/
- **MODIS Data**: https://modis.gsfc.nasa.gov/
- **Landsat**: https://landsat.gsfc.nasa.gov/
- **Earth Data Science Textbook**: https://www.earthdatascience.org/

## Installation

```bash
# Install EarthPy and dependencies
conda install -c conda-forge earthpy

# Or with pip (requires GDAL)
pip install earthpy
```

**Note**: GDAL can be challenging to install. Consider using conda for easier dependency management.

