#!/usr/bin/env python
"""
Ingest NYC taxi data into PostgreSQL database.

Usage:
    python ingest_data.py --pg-host localhost --pg-user root --pg-pass root \
        --pg-db ny_taxi --target-table yellow_taxi_data --year 2021 --month 1
"""
import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm


# Define data types for yellow taxi data
DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "object",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

PARSE_DATES = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


def ingest_data(url: str, engine, target_table: str, chunksize: int = 100000):
    """Ingest data from CSV to PostgreSQL in chunks."""
    click.echo(f"Downloading data from: {url}")
    
    df_iter = pd.read_csv(
        url,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=chunksize,
    )

    # Process first chunk to create table schema
    first_chunk = next(df_iter)
    first_chunk.to_sql(name=target_table, con=engine, if_exists="replace", index=False)
    click.echo(f"Created table '{target_table}' and inserted first chunk: {len(first_chunk)} rows")

    # Process remaining chunks
    for df_chunk in tqdm(df_iter, desc="Ingesting chunks"):
        df_chunk.to_sql(name=target_table, con=engine, if_exists="append", index=False)

    click.echo(f"✅ Data ingestion to '{target_table}' completed successfully!")


@click.command()
@click.option("--pg-host", default="localhost", help="PostgreSQL host")
@click.option("--pg-user", default="root", help="PostgreSQL username")
@click.option("--pg-pass", default="root", help="PostgreSQL password")
@click.option("--pg-db", default="ny_taxi", help="PostgreSQL database name")
@click.option("--pg-port", default=5432, type=int, help="PostgreSQL port")
@click.option("--target-table", default="yellow_taxi_data", help="Target table name")
@click.option("--year", default=2021, type=int, help="Year of the data")
@click.option("--month", default=1, type=int, help="Month of the data (1-12)")
@click.option("--chunksize", default=100000, type=int, help="Chunk size for reading CSV")
def main(pg_host, pg_user, pg_pass, pg_db, pg_port, target_table, year, month, chunksize):
    """Ingest NYC Yellow Taxi data into PostgreSQL."""
    # Create database engine
    connection_string = f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_engine(connection_string)
    
    click.echo(f"Target database: {pg_host}:{pg_port}/{pg_db}")
    click.echo(f"Target table: {target_table}")

    # Construct data URL
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
    url = f"{base_url}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz"

    # Run ingestion
    ingest_data(url=url, engine=engine, target_table=target_table, chunksize=chunksize)


if __name__ == "__main__":
    main()
