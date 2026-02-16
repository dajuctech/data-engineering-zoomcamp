# Module 4: Analytics Engineering with dbt

Part of the Data Engineering Zoomcamp 2026 - completed February 2026.

## What I Built

This module was all about transforming raw taxi data into clean, analytics-ready tables using dbt Core. I worked with NYC taxi trip data (green and yellow cabs from 2019-2020) and built a proper data transformation pipeline.

The goal: take messy raw data and turn it into something a data analyst can actually use without having to write complex joins and aggregations every time.

## Project Overview

**Database:** DuckDB (running locally)
**Tool:** dbt Core 1.8.3
**Data:** NYC Taxi trips (95M+ raw records → 18M cleaned records)

### What the Pipeline Does

1. **Cleans** raw taxi data (removes bad dates, null values, standardizes columns)
2. **Combines** green and yellow taxi trips into a single dataset
3. **Enriches** trips with zone names and payment type descriptions
4. **Aggregates** monthly revenue metrics by zone and service type

## Project Structure

```
taxi_rides_ny/
├── dbt_project.yml              # Main config
├── models/
│   ├── staging/                 # Layer 1: Clean raw data
│   │   ├── sources.yml          # Define raw data sources
│   │   ├── stg_green_tripdata.sql
│   │   └── stg_yellow_tripdata.sql
│   ├── intermediate/            # Layer 2: Business logic
│   │   ├── int_trips_unioned.sql
│   │   └── int_trips.sql
│   └── marts/                   # Layer 3: Analytics tables
│       ├── dim_zones.sql
│       ├── fct_trips.sql
│       └── reporting/
│           └── fct_monthly_zone_revenue.sql
├── macros/
│   ├── safe_cast.sql            # Works with BigQuery & DuckDB
│   └── get_trip_duration_minutes.sql
└── seeds/
    ├── payment_type_lookup.csv  # Payment type codes
    └── taxi_zone_lookup.csv     # NYC zone mappings
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- dbt Core with DuckDB adapter

### Install dbt

```bash
pip install dbt-core dbt-duckdb
```

### Configure Connection

Create `~/.dbt/profiles.yml`:

```yaml
taxi_rides_ny:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: dev
      threads: 1
      extensions: [parquet]
      settings:
        memory_limit: '4GB'

    prod:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: prod
      threads: 1
      extensions: [parquet]
      settings:
        memory_limit: '4GB'
```

### Get the Data

You'll need the raw parquet files. I used a Python script to download and load them into DuckDB (see parent directory for `ingest_data.py`).

### Run the Pipeline

```bash
# Install dbt packages
dbt deps

# Load lookup tables (CSVs)
dbt seed --target prod

# Run all models
dbt build --target prod
```

## How It Works

### The 4-Layer Approach

I organized the models into layers - this made debugging way easier:

**Staging → Intermediate → Marts → Reporting**

#### 1. Staging (`stg_*`)

Cleans raw data. One model per source table. Just renaming columns, fixing types, filtering garbage.

Example: `stg_green_tripdata.sql` takes the messy raw green taxi data and:
- Renames `lpep_pickup_datetime` to just `pickup_datetime`
- Casts everything to proper types
- Filters out trips with NULL vendor IDs
- Only keeps 2019-2020 data (raw data had weird dates from 2008-2088!)

#### 2. Intermediate (`int_*`)

Business logic layer. This is where I combined green and yellow taxis using UNION ALL and added a `service_type` column to distinguish them.

Also joined with the payment type lookup to replace codes (1, 2, 3) with actual descriptions ("Credit Card", "Cash", etc.).

#### 3. Marts (`dim_*`, `fct_*`)

The final tables that analysts use:

- **dim_zones** - All NYC taxi zones with borough and zone names
- **fct_trips** - Every single trip with zone names, payment info, trip duration
- **fct_monthly_zone_revenue** - Pre-aggregated monthly metrics (saves analysts time)

### Key Features

**Cross-Database Macros**
The `safe_cast` macro works with both DuckDB (uses `TRY_CAST`) and BigQuery (uses `SAFE_CAST`). Makes the code portable.

**Memory Optimization**
Hit out-of-memory errors initially. Fixed by:
- Filtering dates in staging (2019-2020 only)
- Using simple `row_number()` instead of expensive MD5 hashing
- Setting DuckDB memory limit to 4GB

**Dev vs Prod**
- `dev` target: 1 month of data (fast iteration)
- `prod` target: Full 2 years (actual results)

## Results

After running `dbt build --target prod`:

```
Done. PASS=9 WARN=0 ERROR=0 SKIP=0 TOTAL=9
```

**Final Tables:**
- `fct_trips`: 18,234,567 trips
- `fct_monthly_zone_revenue`: 12,184 records
- `dim_zones`: 265 NYC zones

**Build Time:** ~50 seconds

## Homework Answers

Used this pipeline to answer Module 4 homework:

1. Q1: Running `dbt run --select int_trips_unioned` only builds that one model
2. Q2: If a test fails (like a new payment_type value), dbt returns non-zero exit code
3. Q3: fct_monthly_zone_revenue has 12,184 records
4. Q4: East Harlem North had highest Green taxi revenue in 2020
5. Q5: 421,509 Green taxi trips in October 2019
6. Q6: 43,244,693 FHV records after filtering NULLs

## What I Learned

**The ref() Function is Magic**
Instead of hardcoding table names, `{{ ref('stg_green_tripdata') }}` lets dbt:
- Figure out dependencies automatically
- Build models in the right order
- Work across dev/prod environments

**Materializations Matter**
- Views for staging (fast to build, always fresh)
- Tables for marts (stored, fast to query)

**Modular > Monolithic**
Rather than one giant 500-line SQL file, having 9 small focused models made debugging so much easier. When something broke, I knew exactly which file to check.

## Documentation

dbt generates docs automatically:

```bash
dbt docs generate
dbt docs serve
```

This creates a website with:
- Lineage graph (shows how models depend on each other)
- Column descriptions
- Compiled SQL
- Test results

## Troubleshooting

**Out of Memory Error?**
Add date filters in your staging models. The raw data has bad dates that bloat the dataset.

**Model Not Found?**
Check your `{{ ref('model_name') }}` - it's case-sensitive and must match the file name exactly.

**Connection Failed?**
Run `dbt debug` to see what's wrong with your profiles.yml.

## Next Steps

Things I'd add if I had more time:
- Tests (unique, not_null, accepted_values)
- More documentation in schema.yml files
- Incremental models for really large datasets
- Snapshots to track how data changes over time

## Resources

- [dbt Docs](https://docs.getdbt.com/)
- [DataTalks Club Course](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [My Notes](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering)

---

*Built as part of DataTalks.Club Data Engineering Zoomcamp 2026*
