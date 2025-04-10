import rasterio
import numpy as np
import pandas as pd
from rasterio.transform import xy

# Load the raster
raster_path = "202001_Global_Walking_Only_Travel_Time_To_Healthcare_ETH.tiff"
with rasterio.open(raster_path) as src:
    data = src.read(1)
    transform = src.transform
    nodata = src.nodata
    print(src.crs)
    bounds = src.bounds  # (minx, miny, maxx, maxy)
    print(f"Bounds: {bounds}")

# Mask out NoData values
mask = data != nodata

# Get indices of valid data
rows, cols = np.where(mask)

# Get corresponding coordinates
coords = [xy(transform, row, col) for row, col in zip(rows, cols)]
longitudes, latitudes = zip(*coords)

# Get travel time values
travel_times = data[rows, cols]

# Create DataFrame
df = pd.DataFrame({
    'latitude': latitudes,
    'longitude': longitudes,
    'walking_time_minutes': travel_times
})

# Preview
print(df.head())

# Optional: Save to CSV
df.to_csv("ethiopia_walking_times.csv", index=False)

