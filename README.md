# Data Engineering Zoomcamp

[![Course](https://img.shields.io/badge/Course-Data%20Engineering%20Zoomcamp-blue)](https://github.com/DataTalksClub/data-engineering-zoomcamp)
[![Cohort](https://img.shields.io/badge/Cohort-2026-orange)](https://courses.datatalks.club/de-zoomcamp-2026/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-24.x-blue.svg)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.x-purple.svg)](https://www.terraform.io/)
[![Kestra](https://img.shields.io/badge/Kestra-1.1-green.svg)](https://kestra.io/)

A hands-on learning journey through the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalks.Club (2026 Cohort). This repository contains my code implementations, workflow definitions, and homework solutions for each module.

## 📋 Table of Contents

- [Progress](#-progress)
- [Architecture Overview](#-architecture-overview)
- [Technologies](#-technologies)
- [Project Structure](#-project-structure)
- [Modules](#-modules)
  - [Module 1: Docker, Terraform & SQL](#module-1-docker-terraform--sql)
  - [Module 2: Workflow Orchestration](#module-2-workflow-orchestration)
- [Getting Started](#-getting-started)
- [Resources](#-resources)

## 📊 Progress

| Module | Topic | Status |
|--------|-------|--------|
| 1 | [Docker, Terraform & SQL](#module-1-docker-terraform--sql) | ✅ Completed |
| 2 | [Workflow Orchestration](#module-2-workflow-orchestration) | ✅ Completed |
| 3 | Data Warehousing (BigQuery) | ⬜ Upcoming |
| 4 | Analytics Engineering (dbt) | ⬜ Upcoming |
| 5 | Batch Processing (Spark) | ⬜ Upcoming |
| 6 | Stream Processing (Kafka) | ⬜ Upcoming |

## 🏗️ Architecture Overview

The course builds a complete data engineering pipeline progressively across modules:

```
Module 1                    Module 2                         Module 3+
────────                    ────────                         ────────
                            Kestra Orchestration
                            ┌─────────────────────┐
NYC Taxi CSV ──→ Docker ──→ │ Extract (wget)      │
                            │   ↓                 │
                PostgreSQL ←│ Load (local ETL)    │         BigQuery
                            │   ↓                 │         (Data Warehouse)
                            │ GCS Upload          │──→        ↓
                            │   ↓                 │         dbt Models
                            │ BigQuery (cloud ELT)│──→        ↓
                            └─────────────────────┘         Dashboards
Terraform ──→ GCS Bucket + BigQuery Dataset
```

**Module 1** laid the foundation: Docker containers, PostgreSQL, SQL, Terraform for GCP.
**Module 2** automated everything: orchestrated pipelines with scheduling, backfills, and cloud ELT.

## 🛠️ Technologies

| Category | Technologies |
|----------|-------------|
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kestra (YAML-based, event-driven) |
| **Languages** | Python, SQL, HCL, YAML |
| **Databases** | PostgreSQL, BigQuery, DuckDB |
| **Cloud** | Google Cloud Platform (GCS, BigQuery) |
| **Infrastructure** | Terraform |
| **Data Processing** | pandas, SQLAlchemy |
| **AI/ML** | Gemini, RAG, Embeddings |
| **Tools** | pgAdmin, Jupyter, UV |

## 📁 Project Structure

```
data-engineering-zoomcamp/
│
├── 01-docker-terraform/                 # Module 1: Docker, Terraform & SQL
│   ├── 01-documentation.md              # Comprehensive module notes
│   ├── week1_2026_answer.md             # Homework solutions
│   │
│   ├── docker-sql/                      # Docker & PostgreSQL
│   │   ├── README.md                    # Setup instructions
│   │   └── pipeline/
│   │       ├── Dockerfile               # Multi-stage Docker build (UV)
│   │       ├── docker-compose.yaml      # PostgreSQL + pgAdmin
│   │       ├── ingest_data.py           # NYC Taxi data ingestion CLI
│   │       ├── notebook.ipynb           # Exploratory data analysis
│   │       └── pyproject.toml           # Python dependencies
│   │
│   ├── queries/                         # SQL Practice
│   │   ├── 01_basic_queries.sql         # SELECT, COUNT, GROUP BY
│   │   ├── 02_join_queries.sql          # JOINs (INNER, LEFT, RIGHT, OUTER)
│   │   ├── 03_group_by_with_joins.sql   # Aggregations with JOINs
│   │   └── 04_check_missing_data.sql    # Data quality checks
│   │
│   └── terraform/                       # Infrastructure as Code
│       ├── README.md                    # Terraform setup guide
│       ├── terraform_basic/             # Hardcoded configuration
│       │   └── main.tf
│       └── terraform_with_variables/    # Parameterized configuration
│           ├── main.tf                  # GCS bucket + BigQuery dataset
│           └── variables.tf             # Configurable variables
│
├── 02-workflow-orchestration/           # Module 2: Workflow Orchestration
│   ├── README.md                        # Setup & usage instructions
│   ├── week2_2026_answer.md             # Homework solutions
│   ├── docker-compose.yml               # Kestra + PostgreSQL + pgAdmin
│   └── flows/                           # Kestra workflow definitions (11 flows)
│       ├── 01_hello_world.yaml          # Basics: tasks, inputs, triggers
│       ├── 02_python.yaml               # Python in Docker containers
│       ├── 03_getting_started_data_pipeline.yaml  # Extract → Transform → Query
│       ├── 04_postgres_taxi.yaml        # ETL: Taxi data → PostgreSQL
│       ├── 05_postgres_taxi_scheduled.yaml  # Scheduled ETL + backfill
│       ├── 06_gcp_kv_from_env.yaml      # GCP KV Store configuration
│       ├── 07_gcp_setup.yaml            # Create GCS bucket + BQ dataset
│       ├── 08_gcp_taxi.yaml             # ELT: Taxi data → GCS → BigQuery
│       ├── 09_gcp_taxi_scheduled.yaml   # Scheduled ELT + backfill
│       ├── 10_chat_without_rag.yaml     # AI without context (hallucinations)
│       └── 11_chat_with_rag.yaml        # AI with RAG (grounded answers)
│
├── .gitignore                           # Git ignore patterns
└── README.md                            # This file
```

## 📚 Modules

### Module 1: Docker, Terraform & SQL

**Status:** ✅ Completed | [Full README](01-docker-terraform/docker-sql/README.md) | [Homework](01-docker-terraform/week1_2026_answer.md)

> **Summary:** Built a containerized data ingestion pipeline that loads 1.3M+ NYC Taxi records into PostgreSQL, then provisioned cloud infrastructure (GCS + BigQuery) with Terraform.

| Topic | What I Learned | Code |
|-------|----------------|------|
| **Docker** | Dockerfile, multi-stage builds, container networking | [Dockerfile](01-docker-terraform/docker-sql/pipeline/Dockerfile) |
| **Docker Compose** | Multi-container orchestration (PostgreSQL + pgAdmin) | [docker-compose.yaml](01-docker-terraform/docker-sql/pipeline/docker-compose.yaml) |
| **Data Ingestion** | Python CLI pipeline with pandas, chunked loading | [ingest_data.py](01-docker-terraform/docker-sql/pipeline/ingest_data.py) |
| **SQL** | JOINs, GROUP BY, aggregations, data quality checks | [Queries](01-docker-terraform/queries/) |
| **GCP Setup** | Service accounts, IAM roles, enabling APIs | [Documentation](01-docker-terraform/01-documentation.md) |
| **Terraform** | Infrastructure as Code — GCS bucket + BigQuery dataset | [Terraform](01-docker-terraform/terraform/) |

<details>
<summary><b>Quick Start - Module 1</b></summary>

```bash
cd 01-docker-terraform/docker-sql/pipeline

# Start PostgreSQL and pgAdmin
docker compose up -d

# Access pgAdmin at http://localhost:8085
# Email: admin@admin.com | Password: root

# Build and run data ingestion
docker build -t taxi-ingest .
docker run --network=pipeline_default taxi-ingest \
  --pg-host pgdatabase --pg-user root --pg-pass root \
  --pg-db ny_taxi --target-table yellow_taxi_data \
  --year 2021 --month 1
```

</details>

---

### Module 2: Workflow Orchestration

**Status:** ✅ Completed | [Full README](02-workflow-orchestration/README.md) | [Homework](02-workflow-orchestration/week2_2026_answer.md)

> **Summary:** Automated the entire data pipeline using Kestra. Built 11 flows covering local ETL to PostgreSQL, cloud ELT to GCS + BigQuery, scheduled execution with backfills, and AI-powered workflow generation with RAG.

| Topic | What I Learned | Code |
|-------|----------------|------|
| **Kestra Fundamentals** | Flows, tasks, inputs, variables, triggers, namespaces | [01_hello_world.yaml](02-workflow-orchestration/flows/01_hello_world.yaml) |
| **Python Orchestration** | Running Python scripts in Docker via Kestra | [02_python.yaml](02-workflow-orchestration/flows/02_python.yaml) |
| **Intro Pipeline** | Extract (HTTP) → Transform (Python) → Query (DuckDB) | [03_getting_started.yaml](02-workflow-orchestration/flows/03_getting_started_data_pipeline.yaml) |
| **ETL to PostgreSQL** | CSV extraction, conditional branching, staging + MERGE | [04_postgres_taxi.yaml](02-workflow-orchestration/flows/04_postgres_taxi.yaml) |
| **Scheduling & Backfills** | Cron triggers, historical data loading | [05_scheduled.yaml](02-workflow-orchestration/flows/05_postgres_taxi_scheduled.yaml) |
| **ETL vs ELT** | Traditional (transform first) vs cloud-native (load first) | [README](02-workflow-orchestration/README.md) |
| **GCP Setup** | KV Store config, GCS bucket + BigQuery dataset creation | [06_kv.yaml](02-workflow-orchestration/flows/06_gcp_kv_from_env.yaml), [07_setup.yaml](02-workflow-orchestration/flows/07_gcp_setup.yaml) |
| **Cloud ELT Pipeline** | GCS upload → External table → MERGE with MD5 dedup | [08_gcp_taxi.yaml](02-workflow-orchestration/flows/08_gcp_taxi.yaml) |
| **Scheduled Cloud ELT** | Staggered cron triggers, trigger.date, backfill at scale | [09_scheduled.yaml](02-workflow-orchestration/flows/09_gcp_taxi_scheduled.yaml) |
| **AI & RAG** | LLM hallucinations, context engineering, RAG with embeddings | [10_no_rag.yaml](02-workflow-orchestration/flows/10_chat_without_rag.yaml), [11_rag.yaml](02-workflow-orchestration/flows/11_chat_with_rag.yaml) |

**Key patterns implemented:**
- **Idempotency** — MD5 hash + MERGE prevents duplicate rows on re-runs
- **Table partitioning** — BigQuery tables partitioned by pickup datetime
- **Conditional branching** — Different schemas for yellow (`tpep_*`) vs green (`lpep_*`) taxis
- **Staggered scheduling** — Green taxis at 9AM UTC, yellow at 10AM UTC
- **Secret management** — KV Store + env variables, never hardcoded credentials

<details>
<summary><b>Quick Start - Module 2</b></summary>

```bash
cd 02-workflow-orchestration

# Configure .env with your GCP credentials (see README)

# Start Kestra + PostgreSQL + pgAdmin
docker compose up -d

# Access Kestra UI at http://localhost:8080
# Email: admin@kestra.io | Password: Admin1234!

# Import all flows
for f in flows/*.yaml; do
  curl -X POST -u 'admin@kestra.io:Admin1234' \
    http://localhost:8080/api/v1/flows/import \
    -F "fileUpload=@$f"
done
```

</details>

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) (24.x or higher)
- [Git](https://git-scm.com/downloads)
- [Terraform](https://www.terraform.io/downloads) (Module 1)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (Modules 1-2)
- GCP service account with `Storage Admin` + `BigQuery Admin` roles

### Environment Setup

**Option 1: GitHub Codespaces (Recommended)**
1. Fork this repository
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. All tools (Docker, Terraform, gcloud) are pre-installed

**Option 2: Local Development**
```bash
git clone https://github.com/YOUR_USERNAME/data-engineering-zoomcamp.git
cd data-engineering-zoomcamp

# Verify Docker is running
docker --version
docker compose version
```

### Data Source

All modules use [NYC Taxi & Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) trip data (yellow and green taxis, 2019-2021) via [DataTalksClub's CSV mirror](https://github.com/DataTalksClub/nyc-tlc-data/releases).

## 🔐 Security

- Credentials (`.env`, `*.json`, service account keys) are in `.gitignore` — never committed
- GCP keys are base64-encoded in env vars and decoded at container runtime
- Kestra KV Store holds non-secret config (project ID, bucket name, dataset)
- All sensitive files verified with `git check-ignore` before every push

## 🔗 Resources

### Official Course Materials
- [Data Engineering Zoomcamp Repository](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Course YouTube Playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
- [DataTalks.Club Slack](https://datatalks.club/slack.html)
- [2026 Cohort Homepage](https://courses.datatalks.club/de-zoomcamp-2026/)

### Documentation
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Kestra Documentation](https://kestra.io/docs)
- [Kestra Plugins (600+)](https://go.kestra.io/de-zoomcamp/plugins)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [BigQuery SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
