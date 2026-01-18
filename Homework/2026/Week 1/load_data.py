import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

# Load green taxi data (parquet)
print("Loading green taxi data...")
df_green = pd.read_parquet('data/green_tripdata_2025-11.parquet')
df_green.to_sql('green_taxi_trips', engine, if_exists='replace', index=False, chunksize=10000)
print(f"Loaded {len(df_green)} green taxi trips")

# Load zone lookup (CSV)
print("Loading zone lookup data...")
df_zones = pd.read_csv('data/taxi_zone_lookup.csv')
df_zones.to_sql('taxi_zones', engine, if_exists='replace', index=False)
print(f"Loaded {len(df_zones)} zones")

print("Data loading complete!")