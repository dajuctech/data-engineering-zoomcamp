# 🚀 Data Engineering Zoomcamp

[![Course](https://img.shields.io/badge/Course-Data%20Engineering%20Zoomcamp-blue)](https://github.com/DataTalksClub/data-engineering-zoomcamp)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-24.x-blue.svg)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.x-purple.svg)](https://www.terraform.io/)

A hands-on learning journey through the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalks.Club. This repository contains my notes, code implementations, and homework solutions for each module.

## 📋 Table of Contents

- [About](#-about)
- [Technologies](#-technologies)
- [Project Structure](#-project-structure)
- [Modules](#-modules)
  - [Module 1: Docker, Terraform & SQL](#module-1-docker-terraform--sql)
  - [Module 2: Workflow Orchestration](#module-2-workflow-orchestration)
- [Getting Started](#-getting-started)
- [Resources](#-resources)

## 🎯 About

This repository documents my progress through the Data Engineering Zoomcamp, a free 9-week course covering:

- **Containerization** with Docker
- **Infrastructure as Code** with Terraform
- **Data Warehousing** with BigQuery
- **Workflow Orchestration** with Kestra
- **Analytics Engineering** with dbt
- **Batch Processing** with Spark
- **Stream Processing** with Kafka

## 🛠️ Technologies

| Category | Technologies |
|----------|-------------|
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kestra |
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
├── 01-docker-terraform/              # Module 1: Docker, Terraform & SQL
│   ├── 01-documentation.md           # 📘 Comprehensive module notes (5500+ lines)
│   ├── week1_2026_answer.md          # ✅ Homework solutions
│   │
│   ├── docker-sql/                   # Docker & PostgreSQL Workshop
│   │   ├── README.md                 # Setup instructions
│   │   └── pipeline/                 # Data ingestion pipeline
│   │       ├── Dockerfile            # Multi-stage Docker build
│   │       ├── docker-compose.yaml   # PostgreSQL + pgAdmin services
│   │       ├── ingest_data.py        # NYC Taxi data ingestion script
│   │       ├── notebook.ipynb        # Exploratory data analysis
│   │       └── pyproject.toml        # Python dependencies (UV)
│   │
│   ├── queries/                      # SQL Practice Queries
│   │   ├── 01_basic_queries.sql      # SELECT, COUNT, GROUP BY
│   │   ├── 02_join_queries.sql       # INNER, LEFT, RIGHT, OUTER JOINs
│   │   ├── 03_group_by_with_joins.sql# Aggregations with JOINs
│   │   └── 04_check_missing_data.sql # Data quality checks
│   │
│   └── terraform/                    # Infrastructure as Code
│       ├── README.md                 # Terraform setup guide
│       ├── terraform_basic/          # Simple hardcoded config
│       │   └── main.tf
│       └── terraform_with_variables/ # Parameterized config
│           ├── main.tf               # GCS bucket + BigQuery dataset
│           └── variables.tf          # Configurable variables
│
├── 02-workflow-orchestration/            # Module 2: Workflow Orchestration
│   ├── README.md                        # Setup & usage instructions
│   ├── week2_2026_answer.md             # ✅ Homework solutions
│   ├── docker-compose.yml               # Kestra + PostgreSQL + pgAdmin
│   └── flows/                           # Kestra workflow definitions
│       ├── 01_hello_world.yaml          # Basics: tasks, inputs, triggers
│       ├── 02_python.yaml               # Python in Docker containers
│       ├── 03_getting_started_data_pipeline.yaml  # Extract → Transform → Query
│       ├── 04_postgres_taxi.yaml        # ETL: Taxi data → PostgreSQL
│       ├── 05_postgres_taxi_scheduled.yaml  # Scheduled ETL + backfill
│       ├── 06_gcp_kv_from_env.yaml      # GCP KV Store configuration
│       ├── 07_gcp_setup.yaml            # Create GCS bucket + BQ dataset
│       ├── 08_gcp_taxi.yaml             # ELT: Taxi data → GCS → BigQuery
│       ├── 09_gcp_taxi_scheduled.yaml   # Scheduled ELT + backfill
│       ├── 10_chat_without_rag.yaml     # AI without context
│       └── 11_chat_with_rag.yaml        # AI with RAG
│
├── .gitignore                           # Git ignore patterns
└── README.md                            # This file
```

## 📚 Modules

### Module 1: Docker, Terraform & SQL

**Status:** ✅ Completed

| Topic | Description | Resources |
|-------|-------------|-----------|
| **Docker Basics** | Containerization fundamentals, Dockerfile, images | [Documentation](01-docker-terraform/01-documentation.md) |
| **PostgreSQL Setup** | Database in Docker, data persistence | [Pipeline](01-docker-terraform/docker-sql/pipeline/) |
| **Data Ingestion** | Python pipeline for NYC Taxi data (1.3M+ records) | [ingest_data.py](01-docker-terraform/docker-sql/pipeline/ingest_data.py) |
| **Docker Compose** | Multi-container orchestration | [docker-compose.yaml](01-docker-terraform/docker-sql/pipeline/docker-compose.yaml) |
| **SQL Refresher** | JOINs, GROUP BY, aggregations | [Queries](01-docker-terraform/queries/) |
| **GCP Setup** | Service accounts, Cloud Storage, BigQuery | [Documentation](01-docker-terraform/01-documentation.md) |
| **Terraform** | Infrastructure as Code for GCP | [Terraform](01-docker-terraform/terraform/) |

#### Key Skills Acquired

- 🐳 Building and running Docker containers
- 🐘 Setting up PostgreSQL with Docker Compose
- 🐍 Creating data pipelines with Python & pandas
- 📊 Writing complex SQL queries with JOINs
- ☁️ Configuring GCP resources (GCS, BigQuery)
- 🏗️ Provisioning infrastructure with Terraform

---

### Module 2: Workflow Orchestration

**Status:** ✅ Completed

| Topic | Description | Resources |
|-------|-------------|-----------|
| **Workflow Orchestration** | Why orchestration matters, core concepts | [README](02-workflow-orchestration/README.md) |
| **Kestra Fundamentals** | Flows, tasks, inputs, triggers, variables | [Hello World](02-workflow-orchestration/flows/01_hello_world.yaml) |
| **Python Orchestration** | Running Python in Docker via Kestra | [Flow](02-workflow-orchestration/flows/02_python.yaml) |
| **ETL Pipeline (Local)** | NYC Taxi data → PostgreSQL with dedup | [Flow](02-workflow-orchestration/flows/04_postgres_taxi.yaml) |
| **Scheduling & Backfills** | Cron triggers, historical data loading | [Flow](02-workflow-orchestration/flows/05_postgres_taxi_scheduled.yaml) |
| **ETL vs ELT** | Traditional vs cloud-native data loading | [README](02-workflow-orchestration/README.md) |
| **GCP ELT Pipeline** | Taxi data → GCS → BigQuery (external tables, MERGE) | [Flow](02-workflow-orchestration/flows/08_gcp_taxi.yaml) |
| **AI & RAG** | Context engineering, hallucination prevention | [Without RAG](02-workflow-orchestration/flows/10_chat_without_rag.yaml), [With RAG](02-workflow-orchestration/flows/11_chat_with_rag.yaml) |

#### Key Skills Acquired

- 🔄 Building orchestrated data pipelines with Kestra (YAML-as-code)
- 🗄️ ETL to PostgreSQL with staging tables and MERGE deduplication
- ☁️ ELT to GCS + BigQuery with external tables and partitioning
- ⏰ Scheduling pipelines with cron triggers and backfilling historical data
- 🔑 Managing secrets with KV Store and environment variables
- 🤖 Using AI (Gemini) and RAG for context-grounded workflow generation

#### Quick Start - Module 2

```bash
cd data-engineering-zoomcamp/02-workflow-orchestration

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

---

#### Quick Start - Module 1

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/data-engineering-zoomcamp.git
cd data-engineering-zoomcamp/01-docker-terraform/docker-sql/pipeline

# Start PostgreSQL and pgAdmin
docker compose up -d

# Access pgAdmin at http://localhost:8085
# Email: admin@admin.com | Password: root

# Run data ingestion
docker build -t taxi-ingest .
docker run --network=pipeline_default taxi-ingest \
  --pg-host pgdatabase --pg-user root --pg-pass root \
  --pg-db ny_taxi --target-table yellow_taxi_data \
  --year 2021 --month 1
```

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) (24.x or higher)
- [Git](https://git-scm.com/downloads)
- [Terraform](https://www.terraform.io/downloads) (for IaC modules)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (for GCP modules)

### Environment Setup

**Option 1: GitHub Codespaces (Recommended)**
1. Fork this repository
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for the environment to initialize

**Option 2: Local Development**
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/data-engineering-zoomcamp.git
cd data-engineering-zoomcamp

# Verify Docker is running
docker --version
docker compose version
```

## 🔗 Resources

### Official Course Materials
- [Data Engineering Zoomcamp Repository](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Course YouTube Playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
- [DataTalks.Club Slack](https://datatalks.club/slack.html)

### Documentation
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Kestra Documentation](https://kestra.io/docs)
- [Google Cloud Documentation](https://cloud.google.com/docs)

---

<p align="center">
  <b>Happy Learning! 🎓</b>
</p>
