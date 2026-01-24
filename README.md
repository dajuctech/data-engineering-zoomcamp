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
- [Getting Started](#-getting-started)
- [Resources](#-resources)

## 🎯 About

This repository documents my progress through the Data Engineering Zoomcamp, a free 9-week course covering:

- **Containerization** with Docker
- **Infrastructure as Code** with Terraform
- **Data Warehousing** with BigQuery
- **Workflow Orchestration** with Mage/Airflow
- **Analytics Engineering** with dbt
- **Batch Processing** with Spark
- **Stream Processing** with Kafka

## 🛠️ Technologies

| Category | Technologies |
|----------|-------------|
| **Containerization** | Docker, Docker Compose |
| **Languages** | Python, SQL, HCL |
| **Databases** | PostgreSQL, BigQuery |
| **Infrastructure** | Terraform, Google Cloud Platform |
| **Data Processing** | pandas, SQLAlchemy |
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
├── .gitignore                        # Git ignore patterns
└── README.md                         # This file
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
- [Google Cloud Documentation](https://cloud.google.com/docs)

---

<p align="center">
  <b>Happy Learning! 🎓</b>
</p>
