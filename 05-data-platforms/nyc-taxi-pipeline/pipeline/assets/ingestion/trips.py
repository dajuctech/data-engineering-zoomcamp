"""@bruin
name: ingestion.trips
type: python
connection: duckdb-default

materialization:
  type: table
  strategy: append
@bruin"""

import os
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from io import BytesIO

def materialize():
    """
    Download NYC taxi parquet files and return as DataFrame.
    Bruin will automatically insert the returned DataFrame into DuckDB.
    """
    # Get time window from Bruin environment variables
    start_date = datetime.fromisoformat(os.environ["BRUIN_START_DATE"])
    end_date = datetime.fromisoformat(os.environ["BRUIN_END_DATE"])
    
    # Get taxi types from pipeline variables
    variables = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = variables.get("taxi_types", ["yellow"])
    
    print(f"Fetching data from {start_date} to {end_date}")
    print(f"Taxi types: {taxi_types}")
    
    # Generate list of months to download
    months = []
    current = start_date
    while current < end_date:
        months.append(current)
        current += relativedelta(months=1)
    
    # Download and combine all parquet files
    all_dfs = []
    
    for month in months:
        year = month.year
        month_num = month.month
        
        for taxi_type in taxi_types:
            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month_num:02d}.parquet"
            
            print(f"Downloading: {url}")
            
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Read parquet from bytes
                df = pd.read_parquet(BytesIO(response.content))
                
                # Add taxi_type column
                df['taxi_type'] = taxi_type
                
                # Standardize column names (yellow vs green have slightly different schemas)
                # This is a simplified version - you may need to adjust based on actual schemas
                df = df.rename(columns={
                    'tpep_pickup_datetime': 'pickup_datetime',
                    'tpep_dropoff_datetime': 'dropoff_datetime',
                    'lpep_pickup_datetime': 'pickup_datetime',
                    'lpep_dropoff_datetime': 'dropoff_datetime',
                    'PULocationID': 'pickup_location_id',
                    'DOLocationID': 'dropoff_location_id'
                })
                
                # Select only columns we need
                columns_to_keep = [
                    'pickup_datetime', 
                    'dropoff_datetime',
                    'pickup_location_id',
                    'dropoff_location_id',
                    'passenger_count',
                    'trip_distance',
                    'fare_amount',
                    'payment_type',
                    'taxi_type'
                ]
                
                # Keep only columns that exist in this dataset
                df = df[[col for col in columns_to_keep if col in df.columns]]
                
                all_dfs.append(df)
                
                print(f"✓ Downloaded {len(df)} rows from {taxi_type} {year}-{month_num:02d}")
                
            except requests.exceptions.RequestException as e:
                print(f"✗ Failed to download {url}: {e}")
                continue
    
    if not all_dfs:
        raise Exception("No data was downloaded successfully")
    
    # Combine all DataFrames
    final_df = pd.concat(all_dfs, ignore_index=True)
    
    print(f"\nTotal rows to insert: {len(final_df)}")
    
    return final_df