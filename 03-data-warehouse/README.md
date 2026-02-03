# Data Warehouse with BigQuery

Analytical data warehousing using Google BigQuery for the NYC Yellow Taxi trip data. This module covers OLAP concepts, table optimization techniques (partitioning & clustering), BigQuery ML for predictive modeling, and model deployment with TensorFlow Serving.

## 📁 Project Structure

```
03-data-warehouse/
├── README.md                      # This file
├── load_yellow_taxi_data.py       # Download taxi data and upload to GCS
├── week3_2026_answer.md           # Homework questions and answers
└── yellow_tripdata_2024-*.parquet # Local data files (gitignored)
```

## 🚀 Quick Start

### Prerequisites

- Google Cloud Platform account with billing enabled
- GCP project with BigQuery and GCS APIs enabled
- Service account with `Storage Admin` and `BigQuery Admin` roles
- Python 3.8+ with `google-cloud-storage` package

### 1. Configure GCP Credentials

```bash
# Option A: Using service account JSON
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Option B: Using gcloud CLI
gcloud auth application-default login
```

### 2. Update Script Configuration

Edit `load_yellow_taxi_data.py`:

```python
BUCKET_NAME = "your-bucket-name"
CREDENTIALS_FILE = "/path/to/your/credentials.json"
```

### 3. Load Data to GCS

```bash
pip install google-cloud-storage
python load_yellow_taxi_data.py
```

### 4. Create BigQuery Tables

```sql
-- Create External Table (references GCS, no data stored in BQ)
CREATE OR REPLACE EXTERNAL TABLE `project.dataset.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket/yellow_tripdata_2024-*.parquet']
);

-- Create Materialized Table (data stored in BQ, non-partitioned)
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_materialized` AS
SELECT * FROM `project.dataset.yellow_taxi_external`;

-- Create Optimized Table (partitioned + clustered)
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `project.dataset.yellow_taxi_external`;
```

## 🔧 Configuration

### Data Loading Script Options

| Variable | Default | Description |
|----------|---------|-------------|
| `BUCKET_NAME` | `**********` | GCS bucket name |
| `CREDENTIALS_FILE` | `../02-workflow-orchestration/...` | Path to service account JSON |
| `BASE_URL` | NYC TLC CloudFront | Data source URL |
| `MONTHS` | `01-06` | Months to download (Jan-June 2024) |
| `CHUNK_SIZE` | `8MB` | Upload chunk size |

### Dataset Information

| Property | Value |
|----------|-------|
| **Source** | [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| **Format** | Parquet |
| **Period** | January - June 2024 |
| **Records** | ~20.3 million trips |
| **Size** | ~500MB (6 files) |

## 📊 Key Concepts

### OLTP vs OLAP

| Feature | OLTP | OLAP |
|---------|------|------|
| **Purpose** | Transaction processing | Analytical queries |
| **Operations** | INSERT, UPDATE, DELETE | SELECT, aggregations |
| **Data** | Current state | Historical trends |
| **Queries** | Simple, row-based | Complex, column-based |
| **Example** | PostgreSQL, MySQL | BigQuery, Snowflake |

### External Tables vs Native Tables

| Feature | External Table | Native Table |
|---------|---------------|--------------|
| Data Location | GCS bucket | BigQuery storage |
| Query Performance | Slower | Faster |
| Cost Estimation | Cannot estimate | Can estimate |
| Partitioning | Not supported | Supported |
| Clustering | Not supported | Supported |
| Use Case | Data exploration | Production queries |

### Partitioning

Divides a table into segments based on a column value (usually date/time).

**Types:**
- Time-unit column partitioning (DATE, TIMESTAMP, DATETIME)
- Ingestion time partitioning (`_PARTITIONTIME`)
- Integer range partitioning

**Benefits:**
- Reduces data scanned (up to 90%+ reduction)
- Lowers query costs
- Improves query performance

**Limits:** Maximum 4,000 partitions per table

### Clustering

Organizes data within partitions based on column values.

**Benefits:**
- Further reduces data scanned (20-50% additional)
- Optimizes filtering and sorting
- Works best with high-cardinality columns

**Limits:** Up to 4 clustering columns

### BigQuery Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       BigQuery                               │
├──────────────┬──────────────────────────────────────────────┤
│  Dremel      │ Distributed SQL execution engine (tree arch) │
│  Colossus    │ Distributed file system for storage          │
│  Jupiter     │ Petabit network for data shuffling           │
│  Borg        │ Cluster management system                    │
└──────────────┴──────────────────────────────────────────────┘

Separation of storage and compute → serverless model
```

## 🤖 BigQuery ML

Train and deploy machine learning models directly in SQL.

### Model Creation

```sql
-- Create linear regression model for tip prediction
CREATE OR REPLACE MODEL `project.dataset.tip_model`
OPTIONS (
  model_type = 'linear_reg',
  input_label_cols = ['tip_amount'],
  DATA_SPLIT_METHOD = 'AUTO_SPLIT'
) AS
SELECT
  passenger_count,
  trip_distance,
  CAST(PULocationID AS STRING) AS PULocationID,
  CAST(DOLocationID AS STRING) AS DOLocationID,
  payment_type,
  fare_amount,
  tip_amount
FROM `project.dataset.yellow_taxi_materialized`
WHERE fare_amount > 0;
```

### Model Evaluation & Prediction

```sql
-- Evaluate model performance
SELECT * FROM ML.EVALUATE(MODEL `project.dataset.tip_model`);

-- Feature importance
SELECT * FROM ML.FEATURE_INFO(MODEL `project.dataset.tip_model`);

-- Generate predictions
SELECT * FROM ML.PREDICT(MODEL `project.dataset.tip_model`, (
  SELECT * FROM `project.dataset.yellow_taxi_materialized` LIMIT 100
));

-- Explain predictions
SELECT * FROM ML.EXPLAIN_PREDICT(
  MODEL `project.dataset.tip_model`,
  (SELECT * FROM `project.dataset.yellow_taxi_materialized` LIMIT 10),
  STRUCT(3 AS top_k_features)
);
```

### Model Deployment with Docker

```bash
# Authenticate with GCP
gcloud auth login

# Export model to GCS
bq --project_id your-project extract -m dataset.tip_model gs://bucket/tip_model

# Download model locally
mkdir -p serving_dir/tip_model/1
gsutil cp -r gs://bucket/tip_model/* serving_dir/tip_model/1/

# Run TensorFlow Serving
docker run -p 8501:8501 \
  --mount type=bind,source=$(pwd)/serving_dir/tip_model,target=/models/tip_model \
  -e MODEL_NAME=tip_model \
  -t tensorflow/serving

# Test prediction endpoint
curl -X POST http://localhost:8501/v1/models/tip_model:predict \
  -d '{"instances": [{"passenger_count": 1, "trip_distance": 2.5, ...}]}'
```

## 📝 Homework Summary

See [week3_2026_answer.md](week3_2026_answer.md) for detailed solutions with SQL queries.

## 💰 Cost Optimization Tips

1. **Always preview estimated bytes** before running queries
2. **Partition by date columns** used in WHERE clauses
3. **Cluster by columns** frequently used in filters
4. **Use external tables** only for data exploration
5. **Avoid SELECT \*** — specify only needed columns
6. **Set up billing alerts** to avoid surprise charges

**Pricing Reference:**

| Plan | Cost | Notes |
|------|------|-------|
| On-demand | $5 per TB scanned | First 1TB/month free |
| Flat-rate | $2,000/month | 100 dedicated slots |

## 🎥 Video Lectures

| # | Topic | Link |
|---|-------|------|
| 1 | Data Warehouse and BigQuery | [YouTube](https://youtu.be/jrHljAoD6nM) |
| 2 | Partitioning vs Clustering | [YouTube](https://youtu.be/-CqXf7vhhDs) |
| 3 | BigQuery Best Practices | [YouTube](https://youtu.be/k81mLJVX08w) |
| 4 | Internals of BigQuery | [YouTube](https://youtu.be/eduHi1inM4s) |
| 5 | BigQuery Machine Learning | [YouTube](https://youtu.be/B-WtpB0PuG4) |
| 6 | Deploying ML Model | [YouTube](https://youtu.be/BjARzEWaznU) |

## 🔗 Resources

### Official Course Materials

- [Module 3 GitHub](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)
- [Slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit?usp=sharing)
- [Homework Submission](https://courses.datatalks.club/de-zoomcamp-2026/homework/hw3)

### BigQuery Documentation

- [BigQuery ML Tutorials](https://cloud.google.com/bigquery-ml/docs/tutorials)
- [Analytics Reference Patterns](https://cloud.google.com/bigquery-ml/docs/analytics-reference-patterns)
- [Linear Regression Syntax](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-glm)
- [Feature Preprocessing](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-preprocess-overview)

### Community Notes

- [Alvaro Navas's Notes](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/3_data_warehouse.md)
- [Isaac Kargar's Notes](https://kargarisaac.github.io/blog/data%20engineering/jupyter/2022/01/30/data-engineering-w3.html)

## 🧹 Cleanup

```bash
# Delete BigQuery tables
bq rm -f -t project:dataset.yellow_taxi_external
bq rm -f -t project:dataset.yellow_taxi_materialized
bq rm -f -t project:dataset.yellow_taxi_optimized

# Delete GCS data
gsutil rm -r gs://your-bucket/yellow_tripdata_2024-*

# Stop TensorFlow Serving container
docker stop $(docker ps -q --filter ancestor=tensorflow/serving)
```


