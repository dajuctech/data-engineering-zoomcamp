# Module 2 Homework: Workflow Orchestration (2026 Cohort)

## Question 1. Uncompressed file size
**Question**: Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

**Answer**: 128.3 MiB

**How to verify**:
1. Run flow `08_gcp_taxi` in Kestra with inputs: taxi=yellow, year=2020, month=12
2. Once complete, click on the **extract** task
3. Go to the **Outputs** tab
4. Check the file size of `yellow_tripdata_2020-12.csv`

**Explanation**: The extract task downloads the `.gz` file and decompresses it. The output file size shown in Kestra is the uncompressed CSV size, which is 128.3 MiB.

---

## Question 2. Rendered variable value
**Question**: What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?

**Answer**: green_tripdata_2020-04.csv

**How to verify**:
The variable template in the flow is:
```yaml
file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

Substituting the inputs:
- `{{inputs.taxi}}` → `green`
- `{{inputs.year}}` → `2020`
- `{{inputs.month}}` → `04`

Result: `green_tripdata_2020-04.csv`

**Explanation**: Kestra renders the variable by replacing the template expressions with the actual input values at execution time.

---

## Question 3. Yellow Taxi rows for 2020
**Question**: How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

**Answer**: 24,648,499

**How to verify**:
1. Run flow `08_gcp_taxi` for taxi=yellow, year=2020, months 01 through 12 (or use backfill on `09_gcp_taxi_scheduled`)
2. Run the following BigQuery query:

```sql
SELECT COUNT(*) as total_rows
FROM `de-zoomcamp-2025-12345.zoomcamp.yellow_tripdata`
WHERE filename LIKE '%2020%';
```

**Per-month breakdown query**:
```sql
SELECT filename, COUNT(*) as row_count
FROM `de-zoomcamp-2025-12345.zoomcamp.yellow_tripdata`
WHERE filename LIKE '%2020%'
GROUP BY filename
ORDER BY filename;
```

**Explanation**: The total is the sum of rows across all 12 monthly yellow taxi CSV files for 2020, loaded via the Kestra ETL pipeline into BigQuery.

---

## Question 4. Green Taxi rows for 2020
**Question**: How many rows are there for the Green Taxi data for all CSV files in the year 2020?

**Answer**: 1,734,051

**How to verify**:
1. Run flow `08_gcp_taxi` for taxi=green, year=2020, months 01 through 12 (or use backfill on `09_gcp_taxi_scheduled`)
2. Run the following BigQuery query:

```sql
SELECT COUNT(*) as total_rows
FROM `de-zoomcamp-2025-12345.zoomcamp.green_tripdata`
WHERE filename LIKE '%2020%';
```

**Explanation**: Green taxi data has significantly fewer rows than yellow taxi data, reflecting lower usage of green taxis in NYC during 2020.

---

## Question 5. Yellow Taxi rows for March 2021
**Question**: How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

**Answer**: 1,925,152

**How to verify**:
1. Run flow `08_gcp_taxi` with inputs: taxi=yellow, year=2021, month=03
2. Run the following BigQuery query:

```sql
SELECT COUNT(*) as total_rows
FROM `de-zoomcamp-2025-12345.zoomcamp.yellow_tripdata_2021_03`;
```

**Explanation**: This is the row count for the single month of March 2021, loaded from `yellow_tripdata_2021-03.csv`.

---

## Question 6. Timezone configuration in Schedule trigger
**Question**: How would you configure the timezone to New York in a Schedule trigger?

**Answer**: Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration

**Example**:
```yaml
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: America/New_York
```

**Explanation**:
- Kestra uses **IANA timezone identifiers** (e.g., `America/New_York`)
- `EST` is incorrect because it doesn't account for daylight saving time (EDT)
- `UTC-5` is not a valid IANA timezone identifier
- `location` is not a valid property for Schedule triggers

---

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- GCP account with BigQuery and GCS enabled
- Kestra running via docker-compose

### Running Kestra
```bash
cd 02-workflow-orchestration
docker-compose up -d
```

### KV Store Configuration
Set the following KV pairs in Kestra UI (Namespaces > zoomcamp > KV Store):

| Key | Value |
|-----|-------|
| `GCP_CREDS` | GCP service account JSON |
| `GCP_PROJECT_ID` | `de-zoomcamp-2025-12345` |
| `GCP_BUCKET_NAME` | Your GCS bucket name |
| `GCP_DATASET` | `zoomcamp` |
| `GCP_LOCATION` | `US` or your region |

### Create BigQuery Dataset
```bash
bq mk --dataset de-zoomcamp-2025-12345:zoomcamp
```

### Running Flows
- **Manual execution**: Use flow `08_gcp_taxi` with taxi type, year, and month inputs
- **Backfill**: Use flow `09_gcp_taxi_scheduled` triggers tab to backfill date ranges

---

## Flows Used
```
02-workflow-orchestration/
├── docker-compose.yml
└── flows/
    ├── 08_gcp_taxi.yaml          # Manual execution flow
    └── 09_gcp_taxi_scheduled.yaml # Scheduled flow with backfill support
```

---

## Resources
- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/)
- [Course Homepage](https://courses.datatalks.club/de-zoomcamp-2026/)
- [Kestra Documentation](https://kestra.io/docs)
- [NYC TLC Data](https://github.com/DataTalksClub/nyc-tlc-data/releases)
