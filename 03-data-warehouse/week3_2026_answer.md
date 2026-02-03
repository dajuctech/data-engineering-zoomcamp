# Module 3 Homework: Data Warehousing & BigQuery - Answers

## Setup SQL

```sql
-- Create External Table
CREATE OR REPLACE EXTERNAL TABLE `project.dataset.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket/yellow_tripdata_2024-*.parquet']
);

-- Create Materialized Table (non-partitioned, non-clustered)
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_materialized` AS
SELECT * FROM `project.dataset.yellow_taxi_external`;
```

---

## Question 1: Counting records

**What is count of records for the 2024 Yellow Taxi Data?**

```sql
SELECT COUNT(*) FROM `project.dataset.yellow_taxi_materialized`;
```

**Answer: 20,332,093**

---

## Question 2: Data read estimation

**What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**

```sql
-- External Table
SELECT COUNT(DISTINCT PULocationID) FROM `project.dataset.yellow_taxi_external`;

-- Materialized Table
SELECT COUNT(DISTINCT PULocationID) FROM `project.dataset.yellow_taxi_materialized`;
```

**Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table**

*Explanation: External tables cannot estimate data size before execution since data resides in GCS. Materialized tables can estimate based on column metadata.*

---

## Question 3: Understanding columnar storage

**Why are the estimated number of Bytes different?**

```sql
-- Query 1: Single column
SELECT PULocationID FROM `project.dataset.yellow_taxi_materialized`;

-- Query 2: Two columns
SELECT PULocationID, DOLocationID FROM `project.dataset.yellow_taxi_materialized`;
```

**Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

---

## Question 4: Counting zero fare trips

**How many records have a fare_amount of 0?**

```sql
SELECT COUNT(*)
FROM `project.dataset.yellow_taxi_materialized`
WHERE fare_amount = 0;
```

**Answer: 8,333**

---

## Question 5: Partitioning and clustering

**What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?**

```sql
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `project.dataset.yellow_taxi_external`;
```

**Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID**

*Explanation: Partitioning by the filter column (tpep_dropoff_datetime) reduces data scanned. Clustering by VendorID optimizes sorting/ordering operations.*

---

## Question 6: Partition benefits

**What are the estimated bytes for non-partitioned vs partitioned table?**

```sql
-- Non-partitioned (materialized) table
SELECT DISTINCT VendorID
FROM `project.dataset.yellow_taxi_materialized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned table
SELECT DISTINCT VendorID
FROM `project.dataset.yellow_taxi_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

**Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

*Explanation: Partitioning allows BigQuery to scan only the relevant date partitions instead of the entire table.*

---

## Question 7: External table storage

**Where is the data stored in the External Table you created?**

**Answer: GCP Bucket**

*Explanation: External tables do not store data in BigQuery. They reference data stored externally in Google Cloud Storage (GCS bucket).*

---

## Question 8: Clustering best practices

**It is best practice in Big Query to always cluster your data:**

**Answer: False**

*Explanation: Clustering is beneficial when queries frequently filter or aggregate on specific columns. However, clustering adds overhead and may not help if:*
- *Tables are small (< 1 GB)*
- *Queries don't filter on clustered columns*
- *Data is rarely queried*

---

## Question 9: Understanding table scans (No Points)

**Write a SELECT count(*) query FROM the materialized table. How many bytes does it estimate will be read? Why?**

```sql
SELECT COUNT(*) FROM `project.dataset.yellow_taxi_materialized`;
```

**Answer: 0 bytes**

**Why:** BigQuery stores table metadata including row counts. For `COUNT(*)` without any filters, BigQuery retrieves this information directly from metadata without scanning any actual table data. This is a query optimization feature of BigQuery.

---


