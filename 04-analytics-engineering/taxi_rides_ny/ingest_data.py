import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def download_and_convert_files(taxi_type):
    """Download CSV.gz files and convert to Parquet"""
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename

            if parquet_filepath.exists():
                print(f"✓ Skipping {parquet_filename} (already exists)")
                continue

            # Download CSV.gz file
            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            print(f"📥 Downloading {csv_gz_filename}...")
            response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
            response.raise_for_status()

            with open(csv_gz_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"🔄 Converting to Parquet...")
            con = duckdb.connect()
            con.execute(f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()

            # Remove CSV.gz to save space
            csv_gz_filepath.unlink()
            print(f"✅ Completed {parquet_filename}\n")

def create_duckdb_tables():
    """Load Parquet files into DuckDB tables"""
    print("📊 Creating DuckDB tables...")
    
    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green"]:
        print(f"Creating prod.{taxi_type}_tripdata...")
        con.execute(f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """)
        
        # Verify row count
        result = con.execute(f"SELECT COUNT(*) FROM prod.{taxi_type}_tripdata").fetchone()
        print(f"✓ Loaded {result[0]:,} rows into prod.{taxi_type}_tripdata")

    con.close()
    print("\n✅ All data loaded successfully!")

def update_gitignore():
    """Add data/ directory to .gitignore"""
    gitignore_path = Path(".gitignore")
    content = gitignore_path.read_text() if gitignore_path.exists() else ""
    
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n')

if __name__ == "__main__":
    print("🚀 Starting data ingestion...\n")
    
    update_gitignore()
    
    for taxi_type in ["yellow", "green"]:
        print(f"\n{'='*60}")
        print(f"Processing {taxi_type.upper()} taxi data")
        print(f"{'='*60}\n")
        download_and_convert_files(taxi_type)
    
    create_duckdb_tables()
    
    print("\n" + "="*60)
    print("🎉 Data ingestion complete!")
    print("="*60)