# Workflow Orchestration with Kestra

Automated data pipelines for NYC Taxi trip data using [Kestra](https://kestra.io/), an open-source orchestration platform. Pipelines load data into both a local PostgreSQL database and Google Cloud Platform (GCS + BigQuery).

## 📁 Project Structure

```
02-workflow-orchestration/
├── docker-compose.yml                 # Kestra + PostgreSQL + pgAdmin services
├── .env                               # Environment variables (GCP credentials, API keys)
├── week2_2026_answer.md               # Homework solutions
├── README.md                          # This file
└── flows/
    ├── 01_hello_world.yaml            # Kestra basics: tasks, inputs, triggers
    ├── 02_python.yaml                 # Running Python in Docker containers
    ├── 03_getting_started_data_pipeline.yaml  # Extract → Transform → Query (DuckDB)
    ├── 04_postgres_taxi.yaml          # ETL: NYC Taxi data → PostgreSQL
    ├── 05_postgres_taxi_scheduled.yaml # Scheduled ETL with backfill support
    ├── 06_gcp_kv_from_env.yaml        # Configure GCP settings in KV Store
    ├── 07_gcp_setup.yaml              # Create GCS bucket + BigQuery dataset
    ├── 08_gcp_taxi.yaml               # ELT: NYC Taxi data → GCS → BigQuery
    ├── 09_gcp_taxi_scheduled.yaml     # Scheduled ELT with backfill support
    ├── 10_chat_without_rag.yaml       # AI query without context (hallucinations)
    └── 11_chat_with_rag.yaml          # AI query with RAG (grounded answers)
```

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- GCP account with BigQuery and Cloud Storage enabled (for cloud pipelines)
- GCP service account JSON key with roles: `Storage Admin`, `BigQuery Admin`

### 1. Configure Environment Variables

Create a `.env` file in this directory:

```bash
# GCP Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_LOCATION=europe-west2
GCP_BUCKET_NAME=your-unique-bucket-name
GCP_DATASET=zoomcamp
GCP_CREDS=<base64-encoded-service-account-json>

# AI API Keys (optional, for flows 10-11)
GEMINI_API_KEY=your-gemini-api-key
```

To base64-encode your service account key:

```bash
base64 -w 0 path/to/service-account.json
```

### 2. Start Services

```bash
docker compose up -d
```

This starts 4 services:

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| **kestra** | `kestra/kestra:v1.1` | `8080` | Orchestration server + UI |
| **kestra_postgres** | `postgres:18` | — | Kestra internal metadata DB |
| **pgdatabase** | `postgres:18` | `5432` | NYC Taxi data (local pipelines) |
| **pgadmin** | `dpage/pgadmin4` | `8085` | Database UI |

### 3. Access Kestra UI

Open [http://localhost:8080](http://localhost:8080) and login:
- **Email**: `admin@kestra.io`
- **Password**: `Admin1234!`

### 4. Import Flows

Import all flows via the Kestra API:

```bash
for f in flows/*.yaml; do
  curl -X POST -u 'admin@kestra.io:Admin1234' \
    http://localhost:8080/api/v1/flows/import \
    -F "fileUpload=@$f"
done
```

Or import individually from the Kestra UI: **Flows** → **Create** → paste YAML content.

### 5. Configure GCP (for cloud pipelines)

Run flow `06_gcp_kv_from_env` to populate the KV Store from your `.env` variables, then run `07_gcp_setup` to create the GCS bucket and BigQuery dataset.

## 📚 Flows Overview

### Learning Fundamentals (Flows 01-03)

| Flow | Description | Key Concepts |
|------|-------------|--------------|
| `01_hello_world` | Basic flow with 5 tasks | Inputs, variables, triggers, concurrency, plugin defaults |
| `02_python` | Python script in Docker | Docker task runner, `kestra` Python library, outputs |
| `03_getting_started_data_pipeline` | Extract → Transform → Query | HTTP download, Python transformation, DuckDB queries |

### Local ETL Pipelines (Flows 04-05)

| Flow | Description | Key Concepts |
|------|-------------|--------------|
| `04_postgres_taxi` | Load NYC Taxi data into PostgreSQL | CSV extraction, conditional branching (yellow/green), staging tables, MERGE deduplication |
| `05_postgres_taxi_scheduled` | Scheduled version with backfill | Cron triggers, backfilling historical data |

**Pipeline architecture:**

```
NYC Taxi CSV (GitHub) → Extract & Decompress
  → Create Staging Table → Load Monthly Data
    → MERGE into Final Table (MD5 dedup)
```

### Cloud ELT Pipelines (Flows 06-09)

| Flow | Description | Key Concepts |
|------|-------------|--------------|
| `06_gcp_kv_from_env` | Populate KV Store from env vars | KV Store, environment variables |
| `07_gcp_setup` | Create GCS bucket + BigQuery dataset | GCP resource provisioning |
| `08_gcp_taxi` | ELT: Taxi data → GCS → BigQuery | GCS upload, external tables, partitioning, MERGE |
| `09_gcp_taxi_scheduled` | Scheduled ELT with backfill | Staggered cron triggers, `trigger.date` filter |

**Pipeline architecture:**

```
NYC Taxi CSV (GitHub) → Extract (wget + gunzip)
  → Upload to GCS Bucket (Data Lake)
    → BigQuery External Table (reads from GCS)
      → Staging Table (MD5 dedup key + filename)
        → MERGE into Final Partitioned Table
```

**Key design patterns:**
- **Idempotency**: MD5 hash of key fields + `MERGE` prevents duplicate rows on re-runs
- **Partitioning**: Final tables partitioned by pickup datetime for query performance
- **Conditional branching**: Yellow taxis (`tpep_*` fields) and green taxis (`lpep_*` fields, plus `ehail_fee`, `trip_type`) have different schemas
- **Staggered schedules**: Green at 9AM UTC, yellow at 10AM UTC to avoid resource contention

### AI & RAG (Flows 10-11)

| Flow | Description | Key Concepts |
|------|-------------|--------------|
| `10_chat_without_rag` | Query LLM without context | Demonstrates hallucinations from knowledge cutoff |
| `11_chat_with_rag` | Query LLM with RAG | Document ingestion, embeddings, grounded responses |

Requires `GEMINI_API_KEY` in the KV Store. Get one at [Google AI Studio](https://aistudio.google.com/app/apikey).

## 🔧 Kestra Core Concepts

| Concept | Description | Example |
|---------|-------------|---------|
| **Flow** | YAML file defining a pipeline | `id: 08_gcp_taxi` |
| **Namespace** | Logical grouping for flows | `namespace: zoomcamp` |
| **Tasks** | Individual steps in a flow | Shell commands, SQL queries, file uploads |
| **Inputs** | Runtime parameters | `taxi: [yellow, green]`, `year`, `month` |
| **Variables** | Template expressions | `"{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"` |
| **Outputs** | Data passed between tasks | `{{outputs.extract.outputFiles[...]}}` |
| **Triggers** | Automatic execution | `cron: "0 9 1 * *"` (monthly at 9AM UTC) |
| **KV Store** | Centralized key-value storage | `{{kv('GCP_PROJECT_ID')}}` |
| **Plugin Defaults** | Shared config for task types | GCP project ID, location, bucket |
| **Labels** | Execution metadata tags | `backfill: true`, `taxi: green` |

## 🔐 Security

- **Never commit credentials** — `.env`, `*.json`, and key files are in `.gitignore`
- **Base64 encoding** — GCP service account is base64-encoded in `.env` and decoded at container startup into `/tmp/gcp-sa.json`
- **GOOGLE_APPLICATION_CREDENTIALS** — Set automatically by `docker-compose.yml` for GCP plugin authentication
- **KV Store** — Non-secret GCP config (project ID, location, bucket, dataset) stored in Kestra's KV Store

## 📊 Data Source

NYC Taxi trip data (yellow and green) in CSV format from [DataTalksClub's GitHub releases](https://github.com/DataTalksClub/nyc-tlc-data/releases). Available years: 2019, 2020, 2021.

### Data Schemas

**Yellow Taxi** — Key fields:

| Column | Type | Description |
|--------|------|-------------|
| `VendorID` | STRING | Provider (1=CMT, 2=VeriFone) |
| `tpep_pickup_datetime` | TIMESTAMP | Meter engaged time |
| `tpep_dropoff_datetime` | TIMESTAMP | Meter disengaged time |
| `passenger_count` | INTEGER | Number of passengers |
| `trip_distance` | NUMERIC | Distance in miles |
| `PULocationID` | STRING | Pickup taxi zone |
| `DOLocationID` | STRING | Dropoff taxi zone |
| `payment_type` | INTEGER | 1=Credit, 2=Cash, 3=No charge, 4=Dispute |
| `total_amount` | NUMERIC | Total charged to passenger |

**Green Taxi** — Same as yellow, plus:

| Column | Type | Description |
|--------|------|-------------|
| `lpep_pickup_datetime` | TIMESTAMP | Meter engaged (note: `lpep` not `tpep`) |
| `lpep_dropoff_datetime` | TIMESTAMP | Meter disengaged |
| `ehail_fee` | NUMERIC | E-hail fee |
| `trip_type` | STRING | 1=Street-hail, 2=Dispatch |

## 🧹 Cleanup

```bash
# Stop all services
docker compose down

# Stop and remove volumes (deletes all data)
docker compose down -v
```

## 🔗 Resources

- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Module 2 - Workflow Orchestration](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration)
- [Kestra Documentation](https://kestra.io/docs)
- [Kestra Blueprints](https://go.kestra.io/de-zoomcamp/blueprints)
- [Kestra Plugins (600+)](https://go.kestra.io/de-zoomcamp/plugins)
- [Kestra YouTube Playlist](https://go.kestra.io/de-zoomcamp/yt-playlist)
- [NYC TLC Data (CSV)](https://github.com/DataTalksClub/nyc-tlc-data/releases)
