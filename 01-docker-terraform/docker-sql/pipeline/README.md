# NYC Taxi Data Ingestion Pipeline

A containerized data ingestion pipeline that loads NYC Yellow Taxi trip data into PostgreSQL using Python, Docker, and UV package manager.

## 📁 Project Structure

```
pipeline/
├── Dockerfile           # Multi-stage Docker build with UV
├── docker-compose.yaml  # PostgreSQL + pgAdmin orchestration
├── ingest_data.py       # CLI data ingestion script
├── notebook.ipynb       # Exploratory data analysis
├── pyproject.toml       # Python dependencies (UV)
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [UV](https://docs.astral.sh/uv/) (optional, for local development)

### 1. Start the Database Services

```bash
docker compose up -d
```

This starts:
- **PostgreSQL** on port `5432` (user: `root`, password: `root`, database: `ny_taxi`)
- **pgAdmin** on port `8085` (email: `admin@admin.com`, password: `root`)

### 2. Run Data Ingestion

#### Option A: Using Docker (Recommended)

```bash
# Build the ingestion image
docker build -t taxi-ingest .

# Run ingestion (connects to Docker network)
docker run --network=pipeline_default taxi-ingest \
    --pg-host pgdatabase \
    --year 2021 \
    --month 1
```

#### Option B: Using UV (Local Development)

```bash
# Install dependencies
uv sync

# Run ingestion script
uv run python ingest_data.py \
    --pg-host localhost \
    --pg-user root \
    --pg-pass root \
    --pg-db ny_taxi \
    --year 2021 \
    --month 1
```

## 🔧 Configuration

### Ingestion Script Options

| Option | Default | Description |
|--------|---------|-------------|
| `--pg-host` | `localhost` | PostgreSQL host |
| `--pg-port` | `5432` | PostgreSQL port |
| `--pg-user` | `root` | PostgreSQL username |
| `--pg-pass` | `root` | PostgreSQL password |
| `--pg-db` | `ny_taxi` | Database name |
| `--target-table` | `yellow_taxi_data` | Target table name |
| `--year` | `2021` | Data year (2019-2021) |
| `--month` | `1` | Data month (1-12) |
| `--chunksize` | `100000` | Rows per chunk |

### Environment Variables

You can also use environment variables for sensitive data:

```bash
export POSTGRES_USER=root
export POSTGRES_PASSWORD=root
export POSTGRES_DB=ny_taxi
```

## 📊 Accessing pgAdmin

1. Open [http://localhost:8085](http://localhost:8085)
2. Login with `admin@admin.com` / `root`
3. Add a new server:
   - **Host**: `pgdatabase` (or `host.docker.internal` from host)
   - **Port**: `5432`
   - **Username**: `root`
   - **Password**: `root`
   - **Database**: `ny_taxi`

## 🗄️ Data Schema

The `yellow_taxi_data` table contains:

| Column | Type | Description |
|--------|------|-------------|
| `VendorID` | INT | TPEP provider (1=CMT, 2=VeriFone) |
| `tpep_pickup_datetime` | TIMESTAMP | Pickup date and time |
| `tpep_dropoff_datetime` | TIMESTAMP | Dropoff date and time |
| `passenger_count` | INT | Number of passengers |
| `trip_distance` | FLOAT | Trip distance in miles |
| `PULocationID` | INT | Pickup location zone ID |
| `DOLocationID` | INT | Dropoff location zone ID |
| `RatecodeID` | INT | Rate code (1=Standard, 2=JFK, etc.) |
| `payment_type` | INT | Payment method (1=Credit, 2=Cash) |
| `fare_amount` | FLOAT | Base fare |
| `tip_amount` | FLOAT | Tip amount |
| `total_amount` | FLOAT | Total charged amount |

## 🛠️ Development

### Running Jupyter Notebook

```bash
# Install dev dependencies
uv sync --group dev

# Start Jupyter
uv run jupyter notebook
```

### Using pgcli (CLI for PostgreSQL)

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker compose down

# Remove volumes (deletes all data)
docker compose down -v
```

## 📚 Data Source

Data is sourced from the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) via [DataTalksClub's mirror](https://github.com/DataTalksClub/nyc-tlc-data).

## 🔗 Related Resources

- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
