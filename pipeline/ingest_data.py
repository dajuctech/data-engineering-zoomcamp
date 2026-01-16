#!/usr/bin/env python
"""
Ingest NYC taxi data into PostgreSQL database.
"""
import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm


@click.command()
@click.option('--pg-host', required=True, help='PostgreSQL host')
@click.option('--pg-user', required=True, help='PostgreSQL username')
@click.option('--pg-pass', required=True, help='PostgreSQL password')
@click.option('--pg-db', required=True, help='PostgreSQL database name')
@click.option('--pg-port', default=5432, help='PostgreSQL port')
@click.option('--target-table', required=True, help='Target table name')
@click.option('--year', type=int, required=True, help='Year of the data')
@click.option('--month', type=int, required=True, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
def main(pg_host, pg_user, pg_pass, pg_db, pg_port, target_table, year, month, chunksize):
    """Ingest NYC taxi data into PostgreSQL."""
    
    # Construct URL
    url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month:02d}.csv.gz'
    
    # Create database engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # Define data types
    dtype = {
        'VendorID': 'Int64',
        'passenger_count': 'Int64',
        'trip_distance': 'float64',
        'RatecodeID': 'Int64',
        'store_and_fwd_flag': 'object',
        'PULocationID': 'Int64',
        'DOLocationID': 'Int64',
        'payment_type': 'Int64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'improvement_surcharge': 'float64',
        'total_amount': 'float64',
        'congestion_surcharge': 'float64'
    }
    
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
    
    click.echo(f"Downloading data from: {url}")
    click.echo(f"Target database: {pg_host}:{pg_port}/{pg_db}")
    click.echo(f"Target table: {target_table}")
    
    # Create iterator
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )
    
    # Process first chunk to create table
    click.echo("Creating table schema...")
    df_first = next(df_iter)
    df_first.to_sql(name=target_table, con=engine, if_exists='replace', index=False)
    click.echo(f"Inserted first chunk: {len(df_first)} rows")
    
    # Process remaining chunks
    click.echo("Processing remaining chunks...")
    for df_chunk in tqdm(df_iter, desc="Ingesting data"):
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append', index=False)
    
    click.echo("✅ Data ingestion completed successfully!")


if __name__ == '__main__':
    main()
