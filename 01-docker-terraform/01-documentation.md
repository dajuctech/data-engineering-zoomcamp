# 📘 Module 1: Complete Docker & Terraform Workshop Documentation

**Comprehensive Guide to Data Engineering Infrastructure Setup**

---

## 🎯 **Project Overview**

This workshop builds a complete data engineering infrastructure from scratch using Docker and Terraform. You'll learn containerization, data pipelines, database management, and infrastructure as code.

**Technologies Used:**
- 🐳 **Docker** - Containerization platform
- 🐘 **PostgreSQL** - Relational database
- 🐍 **Python** - Data processing with pandas
- 🏗️ **Terraform** - Infrastructure as code
- ☁️ **Google Cloud Platform** - Cloud infrastructure
- 🎨 **pgAdmin** - Database management UI
- 📓 **Jupyter** - Interactive data exploration

**What You'll Build:**
1. ✅ Dockerized Python data pipeline
2. ✅ PostgreSQL database in Docker
3. ✅ NYC Taxi data ingestion (1.3M+ records)
4. ✅ Multi-container orchestration with Docker Compose
5. ✅ pgAdmin web interface
6. ✅ GCP infrastructure with Terraform

---

## 📋 **Prerequisites & Setup**

### **Environment: GitHub Codespaces (Recommended)**

**Why Codespaces?**
- ✅ Pre-configured Docker & Python
- ✅ No local installation needed
- ✅ Works on any device with browser
- ✅ Consistent environment for everyone

**Setup Steps:**

1. **Create GitHub Account** (if needed)
   - Visit github.com
   - Sign up for free

2. **Create New Repository**
   ```
   Repository name: data-engineering-zoomcamp
   Visibility: Public
   ✓ Add a README file
   .gitignore: Python
   ```

3. **Launch Codespace**
   - Click green "Code" button
   - Select "Codespaces" tab
   - Click "Create codespace on main"
   - Wait 1-2 minutes for initialization

4. **Configure Terminal** (Optional)
   ```bash
   # Shorter prompt for easier reading
   echo 'export PS1="\$ "' >> ~/.bashrc
   source ~/.bashrc
   ```

### **Alternative: Local Development**

**Requirements:**
- Docker 24.x+
- Python 3.13+
- Git 2.x+

**Installation:**

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Python 3.13
sudo apt update
sudo apt install python3.13 python3.13-venv
```

**macOS:**
```bash
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Install Python via Homebrew
brew install python@3.13
```

**Windows:**
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Install Python: https://www.python.org/downloads/
- Use PowerShell or WSL2
- **Recommendation:** Use Codespaces for simplest setup

---

## 🐳 **Part 1: Docker Fundamentals**

### **1.1 What is Docker?**

**Core Concept:**

```
┌─────────────────────────────────────────────────┐
│         Host Machine (Your Computer)            │
│  ┌───────────────────────────────────────────┐  │
│  │   Docker Container (Isolated)             │  │
│  │   - Ubuntu 20.04                          │  │
│  │   - Python 3.13                           │  │
│  │   - Custom dependencies                   │  │
│  │   - Your application                      │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  Changes inside container DON'T affect host     │
└─────────────────────────────────────────────────┘
```

**Key Points:**
- 🔒 Containers are **isolated environments**
- 🔄 Containers are **stateless** by default
- 📸 Docker **images** are templates
- 🏃 **Containers** are running instances
- ✅ "It works on my machine" → "It works everywhere"

### **1.2 First Docker Commands**

```bash
# Verify Docker installation
docker --version

# Run hello-world
docker run hello-world

# What happened?
# 1. Docker looked for 'hello-world' image locally
# 2. Didn't find it, downloaded from Docker Hub
# 3. Created container from image
# 4. Ran container (printed message)
# 5. Container exited
```

**Interactive Ubuntu Container:**

```bash
# Run Ubuntu interactively
docker run -it ubuntu

# You're now INSIDE the container!
# Prompt changed to: root@abc123:/#

# Try commands:
whoami          # root
ls              # List files
pwd             # Current directory: /

# Install Python (just for demo)
apt update && apt install python3
python3 --version

# Exit container
exit

# Run again - Python is GONE!
docker run -it ubuntu
python3 --version  # Error: not found

# Why? Containers are stateless!
```

**Python Container:**

```bash
# Run Python 3.13 container
docker run -it python:3.13.11-slim

# You're in Python interactive mode
>>> print("Hello from Docker!")
>>> exit()

# Run with Bash instead
docker run -it --entrypoint=bash python:3.13.11-slim

# Now you have bash shell with Python
python3 --version

# With auto-cleanup (recommended!)
docker run -it --rm --entrypoint=bash python:3.13.11-slim
# --rm automatically removes container on exit
```

### **1.3 Understanding Statelessness**

**Demonstration:**

```bash
# Start Ubuntu
docker run -it --rm ubuntu

# Create a file
echo "Hello Docker" > test.txt
cat test.txt  # Works!

# Exit
exit

# Start again
docker run -it --rm ubuntu
cat test.txt  # Error: No such file

# Why? Fresh container from image each time!
```

**Visual:**

```
Docker Image (frozen template)
    ↓
Container 1 (changes here)
    ↓ exit
Gone forever!
    ↓
Container 2 (fresh start from image)
```

### **1.4 Volume Mapping - Persistent Data**

**Create Test Environment:**

```bash
# Create test directory with files
mkdir test
cd test
touch file1.txt file2.txt file3.txt
echo "Hello from host" > file1.txt
cd ..
```

**Create Python Script** (`test/list_files.py`):

```python
from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"Files in {current_dir}:")

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue
    
    print(f"  - {filepath.name}")
    
    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content.strip()}")
```

**Use Volume Mapping:**

```bash
# Map local 'test' folder to container's '/app/test'
docker run -it --rm \
  -v $(pwd)/test:/app/test \
  --entrypoint=bash \
  python:3.13.11-slim

# Inside container:
cd /app/test
ls -la          # See your files!
python list_files.py

# Create file inside container
echo "Created in Docker" > file4.txt

# Exit container
exit

# Check local folder
ls test/
# file4.txt is there! Changes persisted!
```

**Volume Mapping Syntax:**

```
-v [HOST_PATH]:[CONTAINER_PATH]

Examples:
-v $(pwd)/test:/app/test              # Current directory
-v /home/user/data:/data              # Absolute path
-v my_named_volume:/app/data          # Named volume (Docker-managed)
```

### **1.5 Container Management**

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Remove specific container
docker rm <container_id>

# Remove ALL stopped containers
docker rm $(docker ps -aq)

# Best practice: Use --rm flag
docker run -it --rm ubuntu
# Container auto-deleted on exit
```

---

## 🐍 **Part 2: Python Virtual Environments with `uv`**

### **2.1 The Problem: Dependency Conflicts**

**Without Virtual Environments:**

```bash
# Global Python installation
pip install pandas==1.5.0    # Project A needs this
pip install pandas==2.0.0    # Project B needs this

# Project A now breaks! 💥
```

**Visual:**

```
❌ WITHOUT VIRTUAL ENVIRONMENTS:
┌────────────────────────────────┐
│   System Python (Messy!)       │
│   pandas 2.0.0 (latest)        │
│   numpy 1.24                   │
│   sqlalchemy 2.0               │
│   ... hundreds more ...        │
│   (All projects share these)   │
└────────────────────────────────┘

✅ WITH VIRTUAL ENVIRONMENTS:
┌──────────────────────────────────┐
│       System Python (Clean)      │
│                                  │
│  ┌──────────┐    ┌──────────┐   │
│  │Project A │    │Project B │   │
│  │pandas 1.5│    │pandas 2.0│   │
│  │numpy 1.23│    │numpy 1.24│   │
│  └──────────┘    └──────────┘   │
└──────────────────────────────────┘
```

### **2.2 Why `uv`?**

| Feature | pip | conda | `uv` |
|---------|-----|-------|------|
| Speed | Slow | Very Slow | ⚡ **10-100x Faster** |
| Lock Files | No | Yes | Yes |
| Virtual Env | Manual | Manual | **Automatic** |
| Written In | Python | Python | **Rust** |

### **2.3 Using `uv`**

**Installation:**

```bash
pip install uv
uv --version
```

**Create Project:**

```bash
mkdir pipeline
cd pipeline

# Initialize with Python 3.13
uv init --python=3.13
```

**Files Created:**

```
pipeline/
├── .python-version      # Specifies Python 3.13
├── pyproject.toml      # Project config & dependencies
├── uv.lock             # Exact dependency versions
└── hello.py            # Sample file (deletable)
```

**Add Dependencies:**

```bash
# Add runtime dependencies
uv add pandas pyarrow

# Add development-only dependencies
uv add --dev jupyter pgcli

# Check what was added
cat pyproject.toml
```

**`pyproject.toml` Structure:**

```toml
[project]
name = "pipeline"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "pandas>=2.2.3",
    "pyarrow>=18.1.0",
]

[dependency-groups]
dev = [
    "jupyter>=1.1.1",
    "pgcli>=4.2.0",
]
```

**Run Commands:**

```bash
# Run Python in virtual environment
uv run python -V

# Compare with system Python
python -V

# Run your script
uv run python pipeline.py

# Manual activation (alternative)
source .venv/bin/activate
python pipeline.py
deactivate
```

---

## 📊 **Part 3: Building the Data Pipeline**

### **3.1 Simple Pipeline Script**

Create `pipeline/pipeline.py`:

```python
import sys
import pandas as pd

# Get command-line argument
day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

# Create sample DataFrame
df = pd.DataFrame({
    "day": [day],
    "number_passengers": [100],
    "trip_distance": [5.2]
})

# Add month column
month = 1
df['month'] = month

# Display data
print(df.head())

# Save to Parquet
output_file = f"output_day_{day}.parquet"
df.to_parquet(output_file)
print(f"Saved to {output_file}")
```

**Run It:**

```bash
# Install dependencies
uv add pandas pyarrow

# Execute pipeline
uv run python pipeline.py 12
```

**Output:**
```
Running pipeline for day 12
   day  number_passengers  trip_distance  month
0   12                100            5.2      1
Saved to output_day_12.parquet
```

**Git Configuration:**

```bash
# Don't commit binary files
echo "*.parquet" >> .gitignore

# Commit code
git add pipeline.py pyproject.toml uv.lock .gitignore
git commit -m "Add simple pipeline"
```

---

## 🐋 **Part 4: Dockerizing the Pipeline**

### **4.1 Create Dockerfile**

Create `pipeline/Dockerfile`:

```dockerfile
# Base image: slim Python 3.13
FROM python:3.13.11-slim

# Copy uv binary from official image (multi-stage build)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /code

# Add virtual environment to PATH
ENV PATH="/code/.venv/bin:$PATH"

# Copy dependency files FIRST (better caching)
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies from lock file
RUN uv sync --locked

# Copy application code LAST
COPY pipeline.py .

# Set entry point
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
```

**Why This Order?**

```
┌─────────────────────────────────────┐
│ Layer 6: COPY pipeline.py          │ ← Changes often
├─────────────────────────────────────┤
│ Layer 5: RUN uv sync               │ ← Changes when deps change
├─────────────────────────────────────┤
│ Layer 4: COPY pyproject.toml ...   │ ← Changes when deps change
├─────────────────────────────────────┤
│ Layer 3: ENV PATH=...              │ ← Rarely changes
├─────────────────────────────────────┤
│ Layer 2: WORKDIR /code             │ ← Rarely changes
├─────────────────────────────────────┤
│ Layer 1: COPY --from uv            │ ← Rarely changes
├─────────────────────────────────────┤
│ Layer 0: FROM python:3.13.11-slim  │ ← Rarely changes
└─────────────────────────────────────┘

Docker caches layers → Faster rebuilds!
```

### **4.2 Build & Run**

```bash
cd pipeline

# Build image
docker build -t test:pandas .

# Run container with argument
docker run -it --rm test:pandas 12
```

**Expected Output:**
```
Running pipeline for day 12
   day  number_passengers  trip_distance  month
0   12                100            5.2      1
Saved to output_day_12.parquet
```

---

## 🗄️ **Part 5: PostgreSQL in Docker**

### **5.1 Why Docker for Databases?**

**Before Docker:**
- ❌ Install PostgreSQL on system
- ❌ Configure manually
- ❌ Version conflicts possible
- ❌ Difficult cleanup

**With Docker:**
- ✅ Run any PostgreSQL version instantly
- ✅ No system-level installation
- ✅ Isolated from other databases
- ✅ Easy cleanup

### **5.2 Run PostgreSQL Container**

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

**Parameter Breakdown:**

| Flag | Purpose | Example |
|------|---------|---------|
| `-e` | Environment variable (configuration) | `-e POSTGRES_USER="root"` |
| `-v` | Volume mapping (data persistence) | `-v name:/path` |
| `-p` | Port mapping (external access) | `-p 5432:5432` |
| `postgres:18` | Image name & version | PostgreSQL 18 |

**Port Mapping Visual:**

```
┌─────────────────────────────────────┐
│     Your Computer (Host)            │
│                                     │
│   Application → localhost:5432      │
│                       ↓             │
│              Port Mapping (-p)      │
│                       ↓             │
│        ┌──────────────────────┐    │
│        │  Docker Container    │    │
│        │  PostgreSQL:5432     │    │
│        └──────────────────────┘    │
└─────────────────────────────────────┘
```

**Expected Output:**
```
PostgreSQL init process complete; ready for start up.

2025-01-24 10:15:30 UTC [1] LOG:  starting PostgreSQL 18.1
2025-01-24 10:15:30 UTC [1] LOG:  listening on IPv4 "0.0.0.0", port 5432
2025-01-24 10:15:30 UTC [1] LOG:  database system is ready to accept connections
```

⚠️ **Leave this terminal running!** Open new terminal for next steps.

### **5.3 Connect with pgcli**

```bash
# In new terminal, navigate to pipeline
cd pipeline

# Install pgcli as dev dependency
uv add --dev pgcli

# Connect to PostgreSQL
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
# Password: root
```

**Basic SQL Commands:**

```sql
-- List tables
\dt

-- Create test table
CREATE TABLE test (
    id INTEGER,
    name VARCHAR(50)
);

-- Insert data
INSERT INTO test VALUES (1, 'Hello Docker');
INSERT INTO test VALUES (2, 'Data Engineering');
INSERT INTO test VALUES (3, 'is awesome!');

-- Query data
SELECT * FROM test;

-- Exit
\q
```

**Test Data Persistence:**

```bash
# Stop PostgreSQL (Ctrl+C in its terminal)

# Start PostgreSQL again with SAME volume name
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# In another terminal, reconnect
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

# Your data is still there!
SELECT * FROM test;
```
I'll continue with the remaining sections of the comprehensive Module 1 documentation.

---

## 📊 **Part 6: NYC Taxi Data Ingestion**

### **6.1 Understanding the Dataset**

**Dataset Information:**
- **Source:** NYC Taxi & Limousine Commission (TLC)
- **Data Type:** Yellow Taxi Trip Records
- **Format:** CSV (gzip compressed)
- **Size:** ~1.3 million records per month
- **Time Period:** January 2021

**Data Dictionary:**

| Column | Type | Description |
|--------|------|-------------|
| `VendorID` | Integer | Provider (1=Creative Mobile, 2=VeriFone) |
| `tpep_pickup_datetime` | Timestamp | Trip start time |
| `tpep_dropoff_datetime` | Timestamp | Trip end time |
| `passenger_count` | Integer | Number of passengers |
| `trip_distance` | Float | Distance in miles |
| `RatecodeID` | Integer | Rate type (1=Standard, 2=JFK, etc.) |
| `store_and_fwd_flag` | String | Y/N - stored trip data |
| `PULocationID` | Integer | Pickup location zone ID |
| `DOLocationID` | Integer | Drop-off location zone ID |
| `payment_type` | Integer | Payment method (1=Credit card, 2=Cash) |
| `fare_amount` | Float | Base fare |
| `extra` | Float | Extra charges |
| `mta_tax` | Float | MTA tax |
| `tip_amount` | Float | Tip amount |
| `tolls_amount` | Float | Toll charges |
| `improvement_surcharge` | Float | Improvement surcharge |
| `total_amount` | Float | Total charge |
| `congestion_surcharge` | Float | Congestion surcharge |

**Access the Data:**

```bash
# Data URL structure
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_YYYY-MM.csv.gz

# Example for January 2021
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

### **6.2 Data Exploration with Jupyter**

**Install Jupyter:**

```bash
cd pipeline
uv add --dev jupyter
```

**Start Jupyter:**

```bash
uv run jupyter notebook
```

**Access Jupyter:**
- Browser opens automatically at `http://localhost:8888`
- Or manually open the URL shown in terminal

**Create New Notebook:**

1. Click "New" → "Python 3"
2. Rename to `notebook.ipynb`

### **6.3 Initial Data Loading**

**Read Sample Data:**

````python
import pandas as pd

# NYC Taxi data URL
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
file = 'yellow_tripdata_2021-01.csv.gz'
url = prefix + file

# Read first 100 rows
df = pd.read_csv(url, nrows=100)

# Display data
df.head()
````

**Inspect Data Structure:**

````python
# Check data types
print(df.dtypes)

# Check shape
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# Check for nulls
print(df.isnull().sum())
````

**Expected Output:**
```
VendorID                        float64
tpep_pickup_datetime             object
tpep_dropoff_datetime            object
passenger_count                 float64
trip_distance                   float64
...
```

**⚠️ Problem Detected:**
- `VendorID` should be `Int64`, not `float64`
- Datetime columns are `object` (strings), not actual timestamps
- Mixed types warning appears

### **6.4 Data Type Specification**

**Why This Matters:**

```
❌ Without Type Specification:
- Pandas guesses types (often wrong)
- Integers become floats (due to NaN)
- Dates remain strings
- Poor query performance
- Wasted memory

✅ With Type Specification:
- Correct data types
- Proper handling of nulls (Int64 vs float64)
- Datetime parsing
- Better performance
- Smaller memory footprint
```

**Define Data Types:**

````python
# Explicit data types
dtype = {
    "VendorID": "Int64",              # Capital I for nullable integer
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

# Columns to parse as dates
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# Read with proper types
df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)

# Verify types
print(df.dtypes)
````

**Now Check:**

````python
# VendorID is now Int64 (not float64)
print(df['VendorID'].dtype)  # Int64

# Datetime columns are properly parsed
print(df['tpep_pickup_datetime'].dtype)  # datetime64[ns]

# Display sample
df.head()
````

### **6.5 Database Connection with SQLAlchemy**

**Install Dependencies:**

```bash
uv add sqlalchemy psycopg2-binary
```

**Create Database Connection:**

````python
from sqlalchemy import create_engine

# Connection string format:
# postgresql://user:password@host:port/database
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Test connection
engine.connect()
````

**Expected Output:**
```
<sqlalchemy.engine.base.Connection at 0x7f8a1c2d3e50>
```

### **6.6 Generate SQL Schema**

**Preview Table Structure:**

````python
# See what SQL table will be created
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
````

**Output:**
```sql
CREATE TABLE yellow_taxi_data (
    "VendorID" BIGINT,
    tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE,
    tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE,
    passenger_count BIGINT,
    trip_distance FLOAT(53),
    "RatecodeID" BIGINT,
    store_and_fwd_flag TEXT,
    "PULocationID" BIGINT,
    "DOLocationID" BIGINT,
    payment_type BIGINT,
    fare_amount FLOAT(53),
    extra FLOAT(53),
    mta_tax FLOAT(53),
    tip_amount FLOAT(53),
    tolls_amount FLOAT(53),
    improvement_surcharge FLOAT(53),
    total_amount FLOAT(53),
    congestion_surcharge FLOAT(53)
)
```

### **6.7 Create Empty Table**

**Why Create Empty First?**

```
Strategy: Two-Step Process
1. Create table structure (schema only)
2. Insert data in chunks

Benefits:
✅ Verify schema before inserting data
✅ Avoid recreating table for each chunk
✅ Better error handling
✅ Clearer separation of concerns
```

**Create Table:**

````python
# Create table with 0 rows (schema only)
df.head(n=0).to_sql(
    name='yellow_taxi_data',
    con=engine,
    if_exists='replace',  # Drop if exists
    index=False           # Don't include pandas index
)

print("Table created successfully!")
````

**Verify in pgcli:**

```bash
# In separate terminal
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

```sql
-- Check tables
\dt

-- Check table structure
\d yellow_taxi_data

-- Should be empty
SELECT COUNT(*) FROM yellow_taxi_data;
```

### **6.8 Chunked Data Ingestion**

**Why Chunks?**

```
📊 Full Dataset: 1,369,765 rows

❌ Load All at Once:
- Memory: ~500 MB+ in RAM
- Time: Unknown (single operation)
- Progress: No visibility
- Failure: Lose everything
- Debugging: Difficult

✅ Load in Chunks (100,000 rows):
- Memory: ~40 MB per chunk
- Time: ~8 seconds per chunk
- Progress: Clear visibility
- Failure: Only lose current chunk
- Debugging: Easy (know which chunk failed)
```

**Visual Flow:**

```
CSV File (1.3M rows, gzipped)
        ↓
Read Chunk 1 (100k rows)  →  Insert  →  Progress: 7%
Read Chunk 2 (100k rows)  →  Insert  →  Progress: 15%
Read Chunk 3 (100k rows)  →  Insert  →  Progress: 22%
        ...
Read Chunk 14 (69,765 rows) →  Insert  →  Progress: 100%
        ↓
    Complete!
```

**Create Iterator:**

````python
# Create iterator (doesn't load all data)
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,        # Returns iterator, not DataFrame
    chunksize=100000      # Read 100k rows at a time
)

# Test: Get first chunk
first_chunk = next(df_iter)
print(f"Chunk size: {len(first_chunk)}")
print(f"Memory usage: {first_chunk.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
````

**Simple Iteration (No Insertion):**

````python
# Just iterate to see progress
for i, df_chunk in enumerate(df_iter, 1):
    print(f"Chunk {i}: {len(df_chunk)} rows")
````

**Insert Data with Progress Bar:**

````python
from tqdm.auto import tqdm

# Install tqdm first
# uv add tqdm

# Recreate iterator (previous one is exhausted)
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)

# Insert chunks with progress bar
for df_chunk in tqdm(df_iter, desc="Inserting data"):
    df_chunk.to_sql(
        name='yellow_taxi_data',
        con=engine,
        if_exists='append',  # Add to existing table
        index=False
    )
    print(f"Inserted {len(df_chunk)} rows")
````

**Alternative: With First Flag:**

````python
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)

first = True

for df_chunk in tqdm(df_iter):
    if first:
        # Create table (first chunk only)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace",
            index=False
        )
        first = False
        print("✓ Table created")
    
    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append",
        index=False
    )
    print(f"✓ Inserted: {len(df_chunk)} rows")
````

**Expected Output:**
```
✓ Table created
✓ Inserted: 100000 rows
✓ Inserted: 100000 rows
✓ Inserted: 100000 rows
...
✓ Inserted: 69765 rows
Complete! Total: 1,369,765 rows
```

### **6.9 Verify Data Ingestion**

**Using pgcli:**

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

```sql
-- Count total rows
SELECT COUNT(*) FROM yellow_taxi_data;
-- Expected: 1,369,765

-- Check date range
SELECT 
    MIN(tpep_pickup_datetime) AS earliest,
    MAX(tpep_pickup_datetime) AS latest
FROM yellow_taxi_data;
-- Expected: 2021-01-01 to 2021-01-31

-- Sample data
SELECT * FROM yellow_taxi_data LIMIT 10;

-- Check for nulls
SELECT 
    COUNT(*) AS total_rows,
    COUNT("PULocationID") AS pickup_locations,
    COUNT("DOLocationID") AS dropoff_locations
FROM yellow_taxi_data;
```

**Using Python:**

````python
# Verify count
query = "SELECT COUNT(*) FROM yellow_taxi_data"
result = pd.read_sql(query, con=engine)
print(f"Total rows: {result.iloc[0, 0]:,}")

# Get sample
query = "SELECT * FROM yellow_taxi_data LIMIT 5"
sample = pd.read_sql(query, con=engine)
print(sample)
````

### **6.10 Performance Considerations**

**Timing Analysis:**

```
Operation               | Time      | Memory
------------------------|-----------|----------
Read full CSV           | 45s       | 500 MB
Read chunk (100k)       | 3s        | 40 MB
Insert chunk            | 8s        | N/A
Total ingestion         | ~2 min    | 40 MB peak

Conclusion: Chunking is 10x more memory efficient!
```

**Optimization Tips:**

1. **Chunk Size Selection:**
   - Too small: Many iterations, slow
   - Too large: Memory issues
   - Sweet spot: 50k-100k rows

2. **Connection Pooling:**
   ````python
   engine = create_engine(
       'postgresql://root:root@localhost:5432/ny_taxi',
       pool_pre_ping=True,  # Verify connections before using
       pool_size=10         # Connection pool size
   )
   ````

3. **Disable Indexes During Insertion:**
   - Create table without indexes
   - Insert all data
   - Create indexes afterward

4. **Use COPY Instead of INSERT:**
   ````python
   # Faster bulk insert
   df_chunk.to_sql(
       name='yellow_taxi_data',
       con=engine,
       if_exists='append',
       index=False,
       method='multi'  # Batch inserts
   )
   ````
I'll continue with the comprehensive Module 1 documentation, picking up where we left off with **Part 7: Creating Ingestion Script** and completing all remaining sections.

---

## 📝 **Part 7: Creating Ingestion Script**

### **7.1 Convert Jupyter Notebook to Python Script**

**Why Convert?**

```
Jupyter Notebooks:
✅ Great for exploration
✅ Interactive development
✅ Visualizations
❌ Not for production
❌ Hard to automate
❌ No CLI arguments

Python Scripts:
✅ Production-ready
✅ Easy to automate
✅ CLI arguments
✅ Version control friendly
✅ Can be containerized
```

**Convert Notebook:**

```bash
# Convert notebook to Python script
uv run jupyter nbconvert --to=script notebook.ipynb

# Rename to something meaningful
mv notebook.py ingest_data.py
```

**Inspect Generated Script:**

````python
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
file = 'yellow_tripdata_2021-01.csv.gz'


# In[3]:


dtype = {
    "VendorID": "Int64",
    # ... rest of types
}
````

**Problems with Generated Script:**

1. Contains Jupyter cell markers (`# In[1]:`)
2. No parameterization
3. Hardcoded values
4. Not production-ready

### **7.2 Clean Up and Parameterize**

**Remove Jupyter Artifacts:**

````python
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# Data types
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]
````

**Add Parameters:**

````python
# Configuration parameters
PG_USER = 'root'
PG_PASSWORD = 'root'
PG_HOST = 'localhost'
PG_PORT = 5432
PG_DB = 'ny_taxi'
TARGET_TABLE = 'yellow_taxi_data'
YEAR = 2021
MONTH = 1
CHUNK_SIZE = 100000
````

### **7.3 Create Main Function**

**Encapsulate Logic:**

````python
def run(pg_user, pg_password, pg_host, pg_port, pg_db, 
        target_table, year, month, chunk_size):
    """Ingest NYC Taxi data into PostgreSQL"""
    
    # Build connection string
    conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
    engine = create_engine(conn_string)
    
    # Build data URL
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    file = f'yellow_tripdata_{year}-{month:02d}.csv.gz'
    url = prefix + file
    
    print(f"📥 Downloading data from: {url}")
    
    # Create iterator
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size
    )
    
    # Ingest data
    first = True
    for df_chunk in tqdm(df_iter, desc="Ingesting data"):
        if first:
            # Create table (first chunk only)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace',
                index=False
            )
            first = False
            print(f"✓ Table '{target_table}' created")
        
        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append',
            index=False
        )
    
    print(f"✓ Data ingestion complete!")
````

### **7.4 Add CLI with Click**

**Why Click?**

```
Built-in Argument Parsing:
❌ sys.argv: Manual parsing, error-prone
✅ argparse: Better, but verbose
✅ Click: Clean, decorator-based, automatic help

Benefits:
- Type validation
- Default values
- Help text generation
- Easy to test
```

**Install Click:**

```bash
uv add click
```

**Add Click Decorators:**

````python
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--year', default=2021, type=int, help='Year')
@click.option('--month', default=1, type=int, help='Month (1-12)')
@click.option('--chunk-size', default=100000, type=int, help='Chunk size for processing')
def run(pg_user, pg_password, pg_host, pg_port, pg_db, 
        target_table, year, month, chunk_size):
    """Ingest NYC Taxi data into PostgreSQL database"""
    
    # Build connection string
    conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
    engine = create_engine(conn_string)
    
    # Build data URL
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    file = f'yellow_tripdata_{year}-{month:02d}.csv.gz'
    url = prefix + file
    
    print(f"📥 Downloading data from: {url}")
    print(f"📊 Target: {pg_host}:{pg_port}/{pg_db}.{target_table}")
    
    # Create iterator
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size
    )
    
    # Ingest data
    first = True
    total_rows = 0
    
    for df_chunk in tqdm(df_iter, desc="Ingesting data"):
        if first:
            # Create table (first chunk only)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace',
                index=False
            )
            first = False
            print(f"✓ Table '{target_table}' created")
        
        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append',
            index=False
        )
        
        total_rows += len(df_chunk)
    
    print(f"✓ Data ingestion complete! Total rows: {total_rows:,}")

if __name__ == '__main__':
    run()
````

### **7.5 Test the Script**

**Basic Test:**

```bash
# Run with default parameters
uv run python ingest_data.py
```

**Custom Parameters:**

```bash
# Run with custom parameters
uv run python ingest_data.py \
  --pg-user=root \
  --pg-password=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips \
  --year=2021 \
  --month=1 \
  --chunk-size=50000
```

**View Help:**

```bash
# See all available options
uv run python ingest_data.py --help
```

**Expected Output:**

```
Usage: ingest_data.py [OPTIONS]

  Ingest NYC Taxi data into PostgreSQL database

Options:
  --pg-user TEXT            PostgreSQL user
  --pg-password TEXT        PostgreSQL password
  --pg-host TEXT            PostgreSQL host
  --pg-port INTEGER         PostgreSQL port
  --pg-db TEXT             PostgreSQL database
  --target-table TEXT      Target table name
  --year INTEGER           Year
  --month INTEGER          Month (1-12)
  --chunk-size INTEGER     Chunk size for processing
  --help                   Show this message and exit.
```

### **7.6 Error Handling**

**Add Try-Except Blocks:**

````python
@click.command()
# ...options...
def run(pg_user, pg_password, pg_host, pg_port, pg_db, 
        target_table, year, month, chunk_size):
    """Ingest NYC Taxi data into PostgreSQL database"""
    
    try:
        # Build connection string
        conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
        engine = create_engine(conn_string)
        
        # Test connection
        engine.connect()
        print(f"✓ Connected to database: {pg_db}")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    try:
        # Build data URL
        prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
        file = f'yellow_tripdata_{year}-{month:02d}.csv.gz'
        url = prefix + file
        
        print(f"📥 Downloading data from: {url}")
        
        # Create iterator
        df_iter = pd.read_csv(
            url,
            dtype=dtype,
            parse_dates=parse_dates,
            iterator=True,
            chunksize=chunk_size
        )
        
    except Exception as e:
        print(f"❌ Failed to download/parse data: {e}")
        return
    
    try:
        # Ingest data
        first = True
        total_rows = 0
        
        for df_chunk in tqdm(df_iter, desc="Ingesting data"):
            if first:
                df_chunk.head(0).to_sql(
                    name=target_table,
                    con=engine,
                    if_exists='replace',
                    index=False
                )
                first = False
                print(f"✓ Table '{target_table}' created")
            
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists='append',
                index=False
            )
            
            total_rows += len(df_chunk)
        
        print(f"✓ Data ingestion complete! Total rows: {total_rows:,}")
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        return
````

---

## 🐳 **Part 8: Dockerizing Ingestion Script**

### **8.1 Update Dockerfile**

**Previous Dockerfile (for pipeline.py):**

````dockerfile
FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY pipeline.py .  # ← Old script

ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
````

**New Dockerfile (for ingest_data.py):**

````dockerfile
FROM python:3.13.11-slim

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /code

# Add venv to PATH
ENV PATH="/code/.venv/bin:$PATH"

# Copy dependency files
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies
RUN uv sync --locked

# Copy ingestion script
COPY ingest_data.py .

# Set entry point
ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]
````

### **8.2 Build Docker Image**

```bash
cd pipeline

# Build with new tag
docker build -t taxi_ingest:v001 .
```

**Expected Output:**

```
[+] Building 45.3s (12/12) FINISHED
 => [internal] load build definition
 => => transferring dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.13.11-slim
 => [1/6] FROM docker.io/library/python:3.13.11-slim
 => [internal] load build context
 => CACHED [2/6] WORKDIR /code
 => [3/6] COPY pyproject.toml .python-version uv.lock ./
 => [4/6] RUN uv sync --locked
 => [5/6] COPY ingest_data.py .
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/taxi_ingest:v001
```

### **8.3 Test Locally First**

**Run Without Network (Will Fail):**

```bash
docker run -it --rm \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=localhost \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```

**Error:**

```
❌ Database connection failed: could not connect to server: Connection refused
```

**Why?** Container's `localhost` ≠ Host's `localhost`

### **8.4 Run with Docker Network**

**Find Docker Compose Network:**

```bash
docker network ls
```

**Output:**

```
NETWORK ID     NAME                DRIVER    SCOPE
abc123...      bridge              bridge    local
def456...      pipeline_default    bridge    local
ghi789...      pg-network          bridge    local
```

**Run on Same Network:**

```bash
docker run -it --rm \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips \
    --year=2021 \
    --month=1
```

**Key Changes:**

- `--network=pipeline_default`: Connect to Docker Compose network
- `--pg-host=pgdatabase`: Use container name (not `localhost`)

**Expected Output:**

```
✓ Connected to database: ny_taxi
📥 Downloading data from: https://...yellow_tripdata_2021-01.csv.gz
📊 Target: pgdatabase:5432/ny_taxi.yellow_taxi_trips
✓ Table 'yellow_taxi_trips' created
Ingesting data: 100%|██████████| 14/14 [02:15<00:00,  9.68s/it]
✓ Data ingestion complete! Total rows: 1,369,765
```

### **8.5 Verify Data in pgAdmin**

**Connect to pgAdmin:**

```
http://localhost:8085
```

**Query:**

```sql
SELECT COUNT(*) FROM yellow_taxi_trips;
-- Expected: 1,369,765

SELECT * FROM yellow_taxi_trips LIMIT 10;
```

---
I'll continue with **Part 9: Docker Compose** and complete all remaining sections comprehensively.

---

## 🐳 **Part 9: Docker Compose - Multi-Container Orchestration**

### **9.1 The Problem with Multiple Containers**

**Current Workflow:**

```bash
# Terminal 1: Run PostgreSQL
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# Terminal 2: Run pgAdmin
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4

# Terminal 3: Run ingestion script
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```

**Problems:**

```
❌ Multiple terminals required
❌ Long commands to remember
❌ Manual network creation
❌ Difficult to manage lifecycle
❌ Error-prone (typos, wrong ports)
❌ Hard to share with team
```

### **9.2 Docker Compose Solution**

**What is Docker Compose?**

```
Docker Compose is a tool for defining and running
multi-container Docker applications.

With Compose, you use a YAML file to configure your
application's services. Then, with a single command,
you create and start all the services.
```

**Benefits:**

```
✅ Single file configuration
✅ One command to start everything
✅ Automatic network creation
✅ Easy service management
✅ Version control friendly
✅ Team collaboration
✅ Environment reproducibility
```

### **9.3 Creating docker-compose.yaml**

**File Location:**

```
pipeline/
├── docker-compose.yaml  ← Create this file
├── Dockerfile
├── ingest_data.py
├── pyproject.toml
└── ...
```

**Complete docker-compose.yaml:**

````yaml
version: '3.8'

services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: ny_taxi
    volumes:
      - ny_taxi_postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - pg-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U root -d ny_taxi"]
      interval: 10s
      timeout: 5s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: root
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    ports:
      - "8085:80"
    networks:
      - pg-network
    depends_on:
      pgdatabase:
        condition: service_healthy

volumes:
  ny_taxi_postgres_data:
  pgadmin_data:

networks:
  pg-network:
    driver: bridge
````

### **9.4 Understanding docker-compose.yaml**

**Section Breakdown:**

**1. Version:**

```yaml
version: '3.8'
```

- Specifies Docker Compose file format version
- `3.8` is compatible with Docker Engine 19.03.0+

**2. Services (Containers):**

```yaml
services:
  pgdatabase:      # Service name (becomes container name)
    image: ...     # Docker image to use
    environment:   # Environment variables
    volumes:       # Volume mappings
    ports:         # Port mappings
    networks:      # Networks to join
```

**3. PostgreSQL Service:**

```yaml
pgdatabase:
  image: postgres:18
  environment:
    POSTGRES_USER: root
    POSTGRES_PASSWORD: root
    POSTGRES_DB: ny_taxi
  volumes:
    - ny_taxi_postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"
  networks:
    - pg-network
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U root -d ny_taxi"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**Healthcheck Explained:**

```
Healthcheck ensures PostgreSQL is fully ready before
dependent services start.

test: Command to check if service is healthy
interval: Check every 10 seconds
timeout: Wait 5 seconds for response
retries: Try 5 times before marking unhealthy
```

**4. pgAdmin Service:**

```yaml
pgadmin:
  image: dpage/pgadmin4
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@admin.com
    PGADMIN_DEFAULT_PASSWORD: root
  volumes:
    - pgadmin_data:/var/lib/pgadmin
  ports:
    - "8085:80"
  networks:
    - pg-network
  depends_on:
    pgdatabase:
      condition: service_healthy
```

**depends_on Explained:**

```
depends_on ensures pgAdmin only starts after PostgreSQL
is healthy (not just running, but accepting connections).

Without condition: Starts after container starts
With condition: Starts after healthcheck passes
```

**5. Volumes:**

```yaml
volumes:
  ny_taxi_postgres_data:  # Named volume for PostgreSQL data
  pgadmin_data:           # Named volume for pgAdmin settings
```

**Why Named Volumes?**

```
Named volumes are managed by Docker:
✅ Persist across container restarts
✅ Easy to backup/restore
✅ Can be shared between containers
✅ Docker manages location
```

**6. Networks:**

```yaml
networks:
  pg-network:
    driver: bridge
```

**Network Types:**

```
bridge: Default, isolated network
host: Share host's network (no isolation)
overlay: Multi-host networking (Swarm/K8s)
none: No networking
```

### **9.5 Docker Compose Commands**

**Start Services:**

```bash
cd pipeline

# Start in foreground (see logs)
docker-compose up

# Start in background (detached mode)
docker-compose up -d
```

**View Logs:**

```bash
# All services
docker-compose logs

# Follow logs (like tail -f)
docker-compose logs -f

# Specific service
docker-compose logs pgdatabase
docker-compose logs pgadmin
```

**Check Status:**

```bash
# List running services
docker-compose ps

# Extended info
docker-compose ps -a
```

**Stop Services:**

```bash
# Stop (containers remain)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers AND volumes
docker-compose down -v
```

**Restart Services:**

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart pgdatabase
```

**Execute Commands in Containers:**

```bash
# Open bash in PostgreSQL container
docker-compose exec pgdatabase bash

# Run psql directly
docker-compose exec pgdatabase psql -U root -d ny_taxi
```

### **9.6 Running Everything with Docker Compose**

**Complete Workflow:**

**1. Start Services:**

```bash
cd pipeline
docker-compose up -d
```

**Expected Output:**

```
Creating network "pipeline_pg-network" with driver "bridge"
Creating volume "pipeline_ny_taxi_postgres_data" with default driver
Creating volume "pipeline_pgadmin_data" with default driver
Creating pipeline_pgdatabase_1 ... done
Creating pipeline_pgadmin_1    ... done
```

**2. Check Status:**

```bash
docker-compose ps
```

**Expected Output:**

```
Name                          Command              State           Ports
----------------------------------------------------------------------------------
pipeline_pgdatabase_1   docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp
pipeline_pgadmin_1      /entrypoint.sh                  Up      0.0.0.0:8085->80/tcp
```

**3. View Logs:**

```bash
docker-compose logs -f
```

**4. Access pgAdmin:**

```bash
# Open browser (or use $BROWSER variable in Codespaces)
"$BROWSER" http://localhost:8085
```

**5. Run Ingestion Script:**

```bash
# Find network name
docker network ls

# Expected: pipeline_pg-network

# Run ingestion
docker run -it --rm \
  --network=pipeline_pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips \
    --year=2021 \
    --month=1
```

**6. Verify Data:**

```bash
# Connect with pgcli
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

# Or use pgAdmin web interface
```

**7. Stop Everything:**

```bash
docker-compose down
```

### **9.7 Adding Ingestion to docker-compose.yaml**

**Optional: Include Ingestion Service**

````yaml
services:
  pgdatabase:
    # ... existing configuration ...

  pgadmin:
    # ... existing configuration ...

  ingest:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      PG_USER: root
      PG_PASSWORD: root
      PG_HOST: pgdatabase
      PG_PORT: 5432
      PG_DB: ny_taxi
      TARGET_TABLE: yellow_taxi_trips
      YEAR: 2021
      MONTH: 1
    networks:
      - pg-network
    depends_on:
      pgdatabase:
        condition: service_healthy
    command: [
      "--pg-user=${PG_USER}",
      "--pg-password=${PG_PASSWORD}",
      "--pg-host=${PG_HOST}",
      "--pg-port=${PG_PORT}",
      "--pg-db=${PG_DB}",
      "--target-table=${TARGET_TABLE}",
      "--year=${YEAR}",
      "--month=${MONTH}"
    ]
````

**Why Not Include Ingestion?**

```
Ingestion typically runs once, not continuously:
- Long-running services: PostgreSQL, pgAdmin
- One-time jobs: Data ingestion

Better approach:
- Use docker-compose for services
- Run ingestion separately as needed
- Or use orchestration tools (Airflow, Prefect)
```

### **9.8 Environment Variables with .env**

**Create .env File:**

````bash
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_DB=ny_taxi

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=root
````

**Update docker-compose.yaml:**

````yaml
services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    # ... rest of config ...

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
    # ... rest of config ...
````

**Benefits:**

```
✅ Sensitive data not in docker-compose.yaml
✅ Easy to change without editing YAML
✅ Can use different .env for dev/prod
✅ .env file can be gitignored
```

**Security Note:**

```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

### **9.9 Docker Compose vs Docker Run**

**Comparison:**

| Feature | docker run | docker-compose |
|---------|-----------|----------------|
| Configuration | Command-line | YAML file |
| Multi-container | Multiple commands | Single command |
| Networking | Manual creation | Automatic |
| Environment vars | `-e` flags | YAML or .env file |
| Volume management | Manual | Declarative |
| Service dependencies | Manual | `depends_on` |
| Reproducibility | Low (long commands) | High (version-controlled) |
| Team collaboration | Difficult | Easy |

### **9.10 Common Docker Compose Patterns**

**Pattern 1: Development Override**

````yaml
# Automatically loaded with docker-compose.yaml

services:
  pgdatabase:
    ports:
      - "5433:5432"  # Different port for dev

  pgadmin:
    environment:
      PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION: 'False'
````

**Pattern 2: Multiple Environments**

```bash
# Development
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up

# Production
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up
```

**Pattern 3: Scaling Services**

```bash
# Run 3 instances of a service
docker-compose up -d --scale worker=3
```

### **9.11 Troubleshooting Docker Compose**

**Common Issues:**

**1. Port Already in Use:**

```bash
# Error: Bind for 0.0.0.0:5432 failed: port is already allocated

# Solution: Find and stop conflicting process
sudo lsof -i :5432
docker-compose down
```

**2. Volume Permissions:**

```bash
# Error: Permission denied

# Solution: Check volume ownership
docker-compose exec pgdatabase ls -la /var/lib/postgresql/data
```

**3. Network Issues:**

```bash
# Error: Cannot connect to database

# Solution: Check network
docker network ls
docker network inspect pipeline_pg-network
```

**4. Service Won't Start:**

```bash
# Check logs
docker-compose logs pgdatabase

# Recreate containers
docker-compose down
docker-compose up -d --force-recreate
```

**5. Healthcheck Failing:**

```bash
# Check healthcheck status
docker-compose ps

# Inspect service
docker inspect pipeline_pgdatabase_1
```

---

## 🔄 **Part 10: SQL Refresher**

### **10.1 Prerequisites**

**Ensure Services Running:**

```bash
cd pipeline
docker-compose up -d
```

**Ensure Data Loaded:**

```bash
# Run ingestion script if needed
docker run -it --rm \
  --network=pipeline_pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```

### **10.2 Connect to Database**

**Using pgcli:**

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

**Using pgAdmin:**

```
http://localhost:8085
```

### **10.3 Basic SELECT Queries**

**View Sample Data:**

```sql
-- Select first 10 rows
SELECT * FROM yellow_taxi_trips
LIMIT 10;

-- Select specific columns
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    total_amount
FROM yellow_taxi_trips
LIMIT 10;

-- Count total rows
SELECT COUNT(*) FROM yellow_taxi_trips;
```

**Expected Output:**

```
┌────────┐
│ count  │
├────────┤
│ 1369765│
└────────┘
```

### **10.4 Filtering with WHERE**

**Basic Filters:**

```sql
-- High-value trips
SELECT *
FROM yellow_taxi_trips
WHERE total_amount > 100
LIMIT 10;

-- Long-distance trips
SELECT *
FROM yellow_taxi_trips
WHERE trip_distance > 50
LIMIT 10;

-- Multiple passengers
SELECT *
FROM yellow_taxi_trips
WHERE passenger_count >= 5
LIMIT 10;
```

**Date Filters:**

```sql
-- Trips on specific date
SELECT *
FROM yellow_taxi_trips
WHERE DATE(tpep_pickup_datetime) = '2021-01-01'
LIMIT 10;

-- Trips in date range
SELECT *
FROM yellow_taxi_trips
WHERE tpep_pickup_datetime BETWEEN '2021-01-01' AND '2021-01-07'
LIMIT 10;
```

**Combining Conditions:**

```sql
-- AND operator
SELECT *
FROM yellow_taxi_trips
WHERE passenger_count >= 3
  AND trip_distance > 10
  AND total_amount > 50
LIMIT 10;

-- OR operator
SELECT *
FROM yellow_taxi_trips
WHERE passenger_count >= 5
   OR trip_distance > 50
LIMIT 10;
```

### **10.5 Aggregate Functions**

**Basic Aggregations:**

```sql
-- Count, Sum, Average, Min, Max
SELECT
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_fare,
    MIN(total_amount) AS min_fare,
    MAX(total_amount) AS max_fare,
    AVG(trip_distance) AS avg_distance
FROM yellow_taxi_trips;
```

**Expected Output:**

```
┌────────────┬───────────────┬──────────┬──────────┬──────────┬──────────────┐
│ trip_count │ total_revenue │ avg_fare │ min_fare │ max_fare │ avg_distance │
├────────────┼───────────────┼──────────┼──────────┼──────────┼──────────────┤
│ 1,369,765  │ 21,234,567.89 │ 15.50    │ -450.00  │ 999.99   │ 5.28         │
└────────────┴───────────────┴──────────┴──────────┴──────────┴──────────────┘
```

### **10.6 GROUP BY - Grouping and Aggregation**

**Group by Single Column:**

```sql
-- Trips per day
SELECT
    DATE(tpep_pickup_datetime) AS pickup_date,
    COUNT(*) AS trip_count,
    AVG(total_amount) AS avg_fare,
    SUM(total_amount) AS total_revenue
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY pickup_date;
```

**Group by Multiple Columns:**

```sql
-- Trips per day and passenger count
SELECT
    DATE(tpep_pickup_datetime) AS pickup_date,
    passenger_count,
    COUNT(*) AS trip_count,
    AVG(total_amount) AS avg_fare
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime), passenger_count
ORDER BY pickup_date, passenger_count;
```

**Using Column Numbers:**

```sql
-- Alternative GROUP BY syntax
SELECT
    DATE(tpep_pickup_datetime) AS pickup_date,
    passenger_count,
    COUNT(*) AS trip_count
FROM yellow_taxi_trips
GROUP BY 1, 2  -- 1 = first column, 2 = second column
ORDER BY 1, 2;
```

### **10.7 ORDER BY - Sorting Results**

**Ascending Order:**

```sql
-- Lowest to highest fares
SELECT
    tpep_pickup_datetime,
    total_amount,
    trip_distance
FROM yellow_taxi_trips
ORDER BY total_amount ASC
LIMIT 10;
```

**Descending Order:**

```sql
-- Highest to lowest fares
SELECT
    tpep_pickup_datetime,
    total_amount,
    trip_distance
FROM yellow_taxi_trips
ORDER BY total_amount DESC
LIMIT 10;
```

**Multiple Sort Columns:**

```sql
-- Sort by distance DESC, then fare ASC
SELECT
    trip_distance,
    total_amount,
    passenger_count
FROM yellow_taxi_trips
ORDER BY trip_distance DESC, total_amount ASC
LIMIT 10;
```

### **10.8 HAVING - Filtering Aggregated Results**

**Difference: WHERE vs HAVING:**

```
WHERE:  Filters rows BEFORE aggregation
HAVING: Filters groups AFTER aggregation
```

**Example:**

```sql
-- Days with more than 50,000 trips
SELECT
    DATE(tpep_pickup_datetime) AS pickup_date,
    COUNT(*) AS trip_count,
    AVG(total_amount) AS avg_fare
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime)
HAVING COUNT(*) > 50000
ORDER BY trip_count DESC;
```

**Multiple HAVING Conditions:**

```sql
-- High-volume, high-revenue days
SELECT
    DATE(tpep_pickup_datetime) AS pickup_date,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_fare
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime)
HAVING COUNT(*) > 50000
   AND SUM(total_amount) > 750000
ORDER BY total_revenue DESC;
```

I'll continue with the comprehensive SQL refresher and remaining sections.

---

### **10.9 Adding Zones Lookup Table**

**Download Zones Data:**

```bash
# Create a zones directory
cd pipeline
mkdir -p data

# Download zones lookup table
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv \
  -O data/taxi_zone_lookup.csv
```

**Create Ingestion Script for Zones:**

````python
import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--zones-url', 
              default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv',
              help='URL to zones CSV')
def run(pg_user, pg_password, pg_host, pg_port, pg_db, zones_url):
    """Ingest NYC Taxi zones lookup table"""
    
    # Build connection string
    conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
    engine = create_engine(conn_string)
    
    print(f"📥 Downloading zones data from: {zones_url}")
    
    # Read zones data
    df_zones = pd.read_csv(zones_url)
    
    print(f"✓ Downloaded {len(df_zones)} zones")
    print(df_zones.head())
    
    # Insert to database
    df_zones.to_sql(
        name='zones',
        con=engine,
        if_exists='replace',
        index=False
    )
    
    print(f"✓ Zones data ingested successfully!")

if __name__ == '__main__':
    run()
````

**Run Zones Ingestion:**

```bash
# Locally
uv run python ingest_zones.py

# Or build and run with Docker
docker build -t zones_ingest:v001 .

docker run -it --rm \
  --network=pipeline_pg-network \
  zones_ingest:v001 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi
```

**Verify Zones Table:**

```sql
-- Check zones table
SELECT * FROM zones LIMIT 10;

-- Count zones
SELECT COUNT(*) FROM zones;
-- Expected: 265 zones
```

### **10.10 SQL JOINS**

**Understanding JOIN Types:**

```
┌─────────────────────────────────────────────┐
│              JOIN Types                     │
├─────────────────────────────────────────────┤
│ INNER JOIN: Only matching rows              │
│ LEFT JOIN:  All from left + matching right  │
│ RIGHT JOIN: All from right + matching left  │
│ FULL OUTER: All rows from both tables       │
└─────────────────────────────────────────────┘
```

**Visual Representation:**

```
Table A (Trips)          Table B (Zones)
┌──────┬────┐             ┌──────┬────────┐
│ ID   │ Loc│             │ ID   │ Name   │
├──────┼────┤             ├──────┼────────┤
│ 1    │ 10 │             │ 10   │ Queens │
│ 2    │ 20 │             │ 20   │ Bronx  │
│ 3    │ 30 │             │ 40   │ Staten │
│ 4    │ 99 │ ← No match  └──────┴────────┘
└──────┴────┘

INNER JOIN: Rows 1, 2, 3 (only matches)
LEFT JOIN:  Rows 1, 2, 3, 4 (all from A)
RIGHT JOIN: Rows 1, 2, 3, + Staten Island row
FULL OUTER: All rows from both tables
```

### **10.11 INNER JOIN**

**Implicit INNER JOIN (Old Style):**

```sql
-- Join trips with pickup zones (comma syntax)
SELECT
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,
    t.total_amount,
    t.trip_distance,
    z."Borough",
    z."Zone"
FROM
    yellow_taxi_trips t,
    zones z
WHERE
    t."PULocationID" = z."LocationID"
LIMIT 100;
```

**Explicit INNER JOIN (Modern Style):**

```sql
-- Same query with explicit JOIN syntax
SELECT
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,
    t.total_amount,
    t.trip_distance,
    z."Borough",
    z."Zone"
FROM
    yellow_taxi_trips t
INNER JOIN
    zones z ON t."PULocationID" = z."LocationID"
LIMIT 100;
```

**Multiple JOINs:**

```sql
-- Join with both pickup AND dropoff zones
SELECT
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,
    t.total_amount,
    CONCAT(zpu."Borough", ' / ', zpu."Zone") AS pickup_loc,
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc
FROM
    yellow_taxi_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
INNER JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

**Expected Output:**

```
┌─────────────────────┬─────────────────────┬──────────────┬────────────────────┬────────────────────┐
│ tpep_pickup_datetime│ tpep_dropoff_datetime│ total_amount │ pickup_loc         │ dropoff_loc        │
├─────────────────────┼─────────────────────┼──────────────┼────────────────────┼────────────────────┤
│ 2021-01-01 00:30:10 │ 2021-01-01 00:36:12 │ 11.80        │ Manhattan / Midtown│ Manhattan / UES    │
│ 2021-01-01 00:51:20 │ 2021-01-01 01:03:17 │ 14.30        │ Queens / Astoria   │ Manhattan / Theater│
└─────────────────────┴─────────────────────┴──────────────┴────────────────────┴────────────────────┘
```

### **10.12 Data Quality Checks**

**Check for NULL Location IDs:**

```sql
-- Find trips with missing location data
SELECT
    COUNT(*) AS trips_with_null_locations
FROM yellow_taxi_trips
WHERE "PULocationID" IS NULL
   OR "DOLocationID" IS NULL;

-- Sample rows with NULL locations
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    "PULocationID",
    "DOLocationID",
    total_amount
FROM yellow_taxi_trips
WHERE "PULocationID" IS NULL
   OR "DOLocationID" IS NULL
LIMIT 10;
```

**Check for Invalid Location IDs:**

```sql
-- Find location IDs not in zones table
SELECT
    COUNT(*) AS trips_with_invalid_locations
FROM yellow_taxi_trips
WHERE "PULocationID" NOT IN (SELECT "LocationID" FROM zones)
   OR "DOLocationID" NOT IN (SELECT "LocationID" FROM zones);

-- Sample invalid locations
SELECT
    tpep_pickup_datetime,
    "PULocationID",
    "DOLocationID",
    total_amount
FROM yellow_taxi_trips
WHERE "PULocationID" NOT IN (SELECT "LocationID" FROM zones)
   OR "DOLocationID" NOT IN (SELECT "LocationID" FROM zones)
LIMIT 10;
```

### **10.13 LEFT JOIN (Outer Join)**

**Purpose: Keep All Trips, Even Without Zone Match**

**Delete a Zone to Demonstrate:**

```sql
-- Delete one zone for demonstration
DELETE FROM zones WHERE "LocationID" = 142;

-- Verify deletion
SELECT * FROM zones WHERE "LocationID" = 142;
-- Should return 0 rows
```

**INNER JOIN (Hides Unmatched Rows):**

```sql
-- INNER JOIN will exclude trips to/from LocationID 142
SELECT
    t.tpep_pickup_datetime,
    t."PULocationID",
    CONCAT(zpu."Borough", ' / ', zpu."Zone") AS pickup_loc
FROM
    yellow_taxi_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE t."PULocationID" = 142
LIMIT 10;

-- Returns 0 rows because zone 142 doesn't exist
```

**LEFT JOIN (Shows All Trips):**

```sql
-- LEFT JOIN keeps all trips, shows NULL for missing zones
SELECT
    t.tpep_pickup_datetime,
    t."PULocationID",
    CONCAT(zpu."Borough", ' / ', zpu."Zone") AS pickup_loc
FROM
    yellow_taxi_trips t
LEFT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE t."PULocationID" = 142
LIMIT 10;

-- Returns trips with NULL in pickup_loc column
```

**Expected Output:**

```
┌─────────────────────┬───────────────┬────────────┐
│ tpep_pickup_datetime│ PULocationID  │ pickup_loc │
├─────────────────────┼───────────────┼────────────┤
│ 2021-01-01 00:30:10 │ 142           │ NULL       │
│ 2021-01-01 00:51:20 │ 142           │ NULL       │
└─────────────────────┴───────────────┴────────────┘
```

**Practical Use Case:**

```sql
-- Find trips with missing zone data
SELECT
    COUNT(*) AS trips_without_zone_info
FROM
    yellow_taxi_trips t
LEFT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE zpu."LocationID" IS NULL;
```

**Handle NULLs with COALESCE:**

```sql
-- Replace NULL with 'Unknown'
SELECT
    t.tpep_pickup_datetime,
    t."PULocationID",
    COALESCE(
        CONCAT(zpu."Borough", ' / ', zpu."Zone"),
        'Unknown Location'
    ) AS pickup_loc
FROM
    yellow_taxi_trips t
LEFT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE t."PULocationID" = 142
LIMIT 10;
```

### **10.14 RIGHT JOIN**

**Rarely Used, But Here's How:**

```sql
-- RIGHT JOIN: Keep all zones, show matching trips
SELECT
    z."LocationID",
    z."Borough",
    z."Zone",
    COUNT(t.*) AS trip_count
FROM
    yellow_taxi_trips t
RIGHT JOIN
    zones z ON t."PULocationID" = z."LocationID"
GROUP BY z."LocationID", z."Borough", z."Zone"
ORDER BY trip_count DESC;

-- Shows all zones, even those with 0 trips
```

### **10.15 FULL OUTER JOIN**

**Keep Everything from Both Tables:**

```sql
-- FULL OUTER JOIN: All trips and all zones
SELECT
    t.tpep_pickup_datetime,
    t."PULocationID",
    z."LocationID",
    z."Zone"
FROM
    yellow_taxi_trips t
FULL OUTER JOIN
    zones z ON t."PULocationID" = z."LocationID"
WHERE t."PULocationID" IS NULL
   OR z."LocationID" IS NULL
LIMIT 100;

-- Shows:
-- - Trips without matching zones
-- - Zones without any trips
```

### **10.16 Aggregation with JOINs**

**Most Popular Pickup Locations:**

```sql
SELECT
    zpu."Borough",
    zpu."Zone",
    COUNT(*) AS pickup_count
FROM
    yellow_taxi_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
GROUP BY zpu."Borough", zpu."Zone"
ORDER BY pickup_count DESC
LIMIT 10;
```

**Average Fare by Pickup Borough:**

```sql
SELECT
    zpu."Borough",
    COUNT(*) AS trip_count,
    AVG(t.total_amount) AS avg_fare,
    AVG(t.trip_distance) AS avg_distance
FROM
    yellow_taxi_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
GROUP BY zpu."Borough"
ORDER BY avg_fare DESC;
```

**Top Routes (Pickup to Dropoff):**

```sql
SELECT
    CONCAT(zpu."Borough", ' → ', zdo."Borough") AS route,
    COUNT(*) AS trip_count,
    AVG(t.total_amount) AS avg_fare,
    AVG(t.trip_distance) AS avg_distance
FROM
    yellow_taxi_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
INNER JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
GROUP BY route
ORDER BY trip_count DESC
LIMIT 10;
```

**Expected Output:**

```
┌────────────────────────┬────────────┬──────────┬──────────────┐
│ route                  │ trip_count │ avg_fare │ avg_distance │
├────────────────────────┼────────────┼──────────┼──────────────┤
│ Manhattan → Manhattan  │ 850,234    │ 12.45    │ 2.1          │
│ Queens → Manhattan     │ 156,789    │ 22.30    │ 8.5          │
│ Brooklyn → Manhattan   │ 89,456     │ 25.60    │ 9.2          │
└────────────────────────┴────────────┴──────────┴──────────────┘
```

### **10.17 Advanced SQL Patterns**

**Window Functions:**

```sql
-- Rank zones by pickup count
SELECT
    zpu."Borough",
    zpu."Zone",
    COUNT(*) AS pickup_count,
    RANK() OVER (PARTITION BY zpu."Borough" ORDER BY COUNT(*) DESC) AS rank_in_borough
FROM
    yellow_taxi_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
GROUP BY zpu."Borough", zpu."Zone"
ORDER BY zpu."Borough", rank_in_borough
LIMIT 20;
```

**Common Table Expressions (CTEs):**

```sql
-- Calculate daily statistics, then find anomalies
WITH daily_stats AS (
    SELECT
        DATE(tpep_pickup_datetime) AS trip_date,
        COUNT(*) AS trip_count,
        AVG(total_amount) AS avg_fare,
        AVG(trip_distance) AS avg_distance
    FROM yellow_taxi_trips
    GROUP BY DATE(tpep_pickup_datetime)
)
SELECT
    trip_date,
    trip_count,
    avg_fare,
    avg_distance
FROM daily_stats
WHERE trip_count > 50000
  AND avg_fare > 15
ORDER BY trip_date;
```

**Subqueries:**

```sql
-- Find trips above average fare
SELECT
    tpep_pickup_datetime,
    total_amount,
    trip_distance
FROM yellow_taxi_trips
WHERE total_amount > (
    SELECT AVG(total_amount)
    FROM yellow_taxi_trips
)
LIMIT 100;
```

### **10.18 SQL Best Practices**

**1. Use Explicit JOINs:**

```sql
-- ❌ Bad (Implicit join)
SELECT * FROM trips t, zones z WHERE t.location_id = z.id;

-- ✅ Good (Explicit join)
SELECT * FROM trips t
INNER JOIN zones z ON t.location_id = z.id;
```

**2. Always Use Table Aliases:**

```sql
-- ❌ Bad (No aliases)
SELECT yellow_taxi_trips.total_amount, zones.Zone
FROM yellow_taxi_trips
INNER JOIN zones ON yellow_taxi_trips."PULocationID" = zones."LocationID";

-- ✅ Good (Clear aliases)
SELECT t.total_amount, z."Zone"
FROM yellow_taxi_trips t
INNER JOIN zones z ON t."PULocationID" = z."LocationID";
```

**3. Filter Early:**

```sql
-- ❌ Bad (Filter after join)
SELECT ...
FROM trips t
INNER JOIN zones z ON t.location_id = z.id
WHERE t.trip_date = '2021-01-01';

-- ✅ Good (Filter before join when possible)
SELECT ...
FROM (
    SELECT * FROM trips WHERE trip_date = '2021-01-01'
) t
INNER JOIN zones z ON t.location_id = z.id;
```

**4. Use LIMIT for Testing:**

```sql
-- Always test with LIMIT first
SELECT ...
FROM large_table
LIMIT 100;

-- Remove LIMIT when query is correct
```

**5. Format for Readability:**

```sql
-- ❌ Bad
SELECT t.pickup,t.dropoff,z.zone FROM trips t INNER JOIN zones z ON t.loc=z.id WHERE t.fare>10;

-- ✅ Good
SELECT
    t.pickup,
    t.dropoff,
    z.zone
FROM trips t
INNER JOIN zones z ON t.loc = z.id
WHERE t.fare > 10;
```

---
I'll continue with **Part 11: GCP Setup** and **Part 12: Terraform**, ensuring comprehensive coverage of everything.

---

## ☁️ **Part 11: Google Cloud Platform (GCP) Setup**

### **11.1 What is Google Cloud Platform?**

**Core Concept:**

```
Google Cloud Platform (GCP) is a suite of cloud computing 
services that runs on the same infrastructure that Google 
uses internally for its end-user products, such as Google 
Search, Gmail, and YouTube.

For Data Engineering:
✅ Scalable data storage (Cloud Storage)
✅ Data warehouse (BigQuery)
✅ Compute resources (Compute Engine, Cloud Run)
✅ Data processing (Dataflow, Dataproc)
✅ Machine Learning (Vertex AI)
```

**Why Use GCP for This Course?**

```
✅ $300 free credits for new accounts
✅ Generous free tier for learning
✅ BigQuery - powerful data warehouse
✅ Industry-standard cloud platform
✅ Easy integration with data tools
```

### **11.2 GCP Service Categories**

**Services We'll Use:**

```
┌─────────────────────────────────────────────┐
│           GCP Services Overview             │
├─────────────────────────────────────────────┤
│                                             │
│  🗄️  Cloud Storage (GCS)                    │
│      - Object storage (like AWS S3)        │
│      - Store CSV, Parquet files            │
│      - Data Lake storage                   │
│                                             │
│  📊 BigQuery                                │
│      - Serverless data warehouse           │
│      - Analyze petabytes of data           │
│      - SQL queries at scale                │
│                                             │
│  💻 Compute Engine                          │
│      - Virtual machines (VMs)              │
│      - Run custom applications             │
│      - Full control over infrastructure    │
│                                             │
└─────────────────────────────────────────────┘
```

### **11.3 Creating a GCP Account**

**Step-by-Step Account Creation:**

**1. Navigate to GCP:**

```
https://cloud.google.com/
```

**2. Click "Get Started for Free":**

- Sign in with Google account (or create one)
- Accept Terms of Service

**3. Billing Information:**

- Country
- Credit/Debit card (required for verification)
- **Note:** You won't be charged during free trial

**4. Free Trial Credits:**

```
You receive:
✅ $300 USD credit (or equivalent in your currency)
✅ Valid for 90 days
✅ No automatic charges after trial ends
✅ Must manually upgrade to paid account
```

**5. Survey (Optional):**

- Skip or fill out for Google's data

### **11.4 Creating Your First Project**

**What is a GCP Project?**

```
A project is a container for:
- All GCP resources
- Billing settings
- API configurations
- Access controls (IAM)
- Service accounts

Think of it as a workspace for your data engineering project.
```

**Create Project:**

**1. From GCP Console:**

```
https://console.cloud.google.com/
```

**2. Click "Select a Project" (top navigation bar)**

**3. Click "New Project":**

```
Project Name:    data-engineering-zoomcamp
Project ID:      de-zoomcamp-412345 (auto-generated, can customize)
Organization:    No organization (for personal projects)
Location:        No organization
```

**4. Click "Create":**

- Takes a few seconds
- Automatically switches to new project

**Project ID vs Project Name:**

```
Project Name:  User-friendly display name (can change)
               Example: "Data Engineering Zoomcamp"

Project ID:    Unique identifier (CANNOT change after creation)
               Example: "de-zoomcamp-412345"
               
Important: Use Project ID in code/config files!
```

**5. Note Your Project ID:**

```bash
# You'll need this for Terraform and other configurations
PROJECT_ID="de-zoomcamp-412345"
```

### **11.5 Understanding IAM (Identity and Access Management)**

**What is IAM?**

```
IAM controls WHO can do WHAT on WHICH resources.

Components:
- Identity: Who (user, service account)
- Role: What permissions
- Resource: Which GCP service/resource
```

**Visual Representation:**

```
┌──────────────────────────────────────────────┐
│              IAM Structure                   │
├──────────────────────────────────────────────┤
│                                              │
│  Identity (Who)                              │
│  └─ User: user@example.com                   │
│  └─ Service Account: terraform@project.iam   │
│                                              │
│  Role (What)                                 │
│  └─ Storage Admin                            │
│  └─ BigQuery Admin                           │
│  └─ Compute Admin                            │
│                                              │
│  Resource (Where)                            │
│  └─ Project: de-zoomcamp-412345              │
│  └─ Bucket: my-data-lake                     │
│  └─ Dataset: taxi_data                       │
│                                              │
└──────────────────────────────────────────────┘
```

### **11.6 Creating a Service Account**

**Why Service Accounts?**

```
Service accounts are special accounts for applications 
(not humans) to authenticate with GCP services.

Use Cases:
✅ Terraform to create infrastructure
✅ Applications to access BigQuery
✅ Data pipelines to read/write Cloud Storage
✅ Automated CI/CD processes
```

**Create Service Account:**

**1. Navigate to IAM & Admin:**

```
Console → Navigation Menu (☰) → IAM & Admin → Service Accounts
```

**Or use search:**

```
Click search bar → Type "Service Accounts" → Select
```

**2. Click "Create Service Account":**

**3. Service Account Details:**

```
Service account name:    terraform-runner
Service account ID:      terraform-runner (auto-generated)
Description:             Service account for Terraform infrastructure deployment
```

**4. Click "Create and Continue":**

**5. Grant Roles (Permissions):**

Add the following roles:

```
Role 1: Storage Admin
  - Full control of GCS buckets and objects
  - Can create, delete, modify buckets
  
Role 2: BigQuery Admin
  - Full control of BigQuery resources
  - Can create datasets, tables, run queries
  
Role 3: Compute Admin
  - Full control of Compute Engine resources
  - Can create, delete VMs
```

**How to Add Roles:**

```
Click "Select a role" dropdown
Search for "Storage Admin" → Select
Click "+ Add Another Role"
Search for "BigQuery Admin" → Select
Click "+ Add Another Role"
Search for "Compute Admin" → Select
```

**6. Click "Continue":**

**7. Grant Users Access (Optional):**

- Skip this for now
- Click "Done"

**Important Security Note:**

```
⚠️ In Production:
- Use least privilege principle
- Grant only necessary permissions
- Use more granular roles:
  ✅ Storage Object Creator (not Storage Admin)
  ✅ BigQuery Data Editor (not BigQuery Admin)
  
For Learning:
- Admin roles are fine
- Easier to avoid permission issues
- Can experiment freely
```

### **11.7 Creating Service Account Keys**

**What are Service Account Keys?**

```
Service account keys are JSON files that contain credentials
allowing applications to authenticate as the service account.

Think of it as a username/password combo in a file.

⚠️ Security Warning:
These keys are HIGHLY sensitive!
- Anyone with this file can act as your service account
- Can create resources and incur charges
- Can access/delete your data
- Should NEVER be committed to Git
- Should NEVER be shared publicly
```

**Create Key:**

**1. From Service Accounts Page:**

```
Find your service account: terraform-runner@...
Click the 3 dots (⋮) on the right
Select "Manage Keys"
```

**2. Add Key:**

```
Click "Add Key" → "Create New Key"
```

**3. Select Key Type:**

```
○ JSON (recommended)
○ P12

Select: JSON
Click "Create"
```

**4. Key Downloaded:**

```
File name: de-zoomcamp-412345-abc123def456.json

⚠️ This file contains sensitive credentials!
The private key will be shown only once.
```

**5. Secure the Key:**

```bash
# Create a keys directory (outside of Git repo)
mkdir -p ~/.gc

# Move the downloaded key
mv ~/Downloads/de-zoomcamp-*.json ~/.gc/ny-rides.json

# Set restrictive permissions
chmod 600 ~/.gc/ny-rides.json
```

**What's Inside the Key File?**

````json
{
  "type": "service_account",
  "project_id": "de-zoomcamp-412345",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "terraform-runner@de-zoomcamp-412345.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
````

### **11.8 Setting Up Authentication**

**Method 1: Environment Variable (Recommended for Development)**

```bash
# Set environment variable pointing to key file
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gc/ny-rides.json"

# Verify it's set
echo $GOOGLE_APPLICATION_CREDENTIALS

# Add to .bashrc to persist across sessions
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gc/ny-rides.json"' >> ~/.bashrc
source ~/.bashrc
```

**Method 2: gcloud CLI Authentication**

```bash
# Authenticate with service account
gcloud auth activate-service-account \
  --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Set project
gcloud config set project de-zoomcamp-412345

# Verify authentication
gcloud auth list

# Test access
gcloud projects describe de-zoomcamp-412345
```

**Method 3: Application Default Credentials (ADC)**

```bash
# For user authentication (uses OAuth)
gcloud auth application-default login

# This opens browser for login
# Credentials stored in:
# ~/.config/gcloud/application_default_credentials.json
```

### **11.9 Installing Google Cloud SDK**

**Why Install gcloud SDK?**

```
✅ Manage GCP resources from command line
✅ Deploy applications
✅ Run local development servers
✅ Authenticate applications
✅ Useful for debugging
```

**Installation:**

**Linux/macOS:**

```bash
# Download and install
curl https://sdk.cloud.google.com | bash

# Restart shell
exec -l $SHELL

# Initialize gcloud
gcloud init
```

**Windows:**

```
Download installer:
https://cloud.google.com/sdk/docs/install

Run: GoogleCloudSDKInstaller.exe
Follow installation wizard
```

**Verify Installation:**

```bash
# Check version
gcloud version

# Expected output:
# Google Cloud SDK 456.0.0
# bq 2.0.97
# core 2024.01.19
# gsutil 5.27
```

**Configure gcloud:**

```bash
# Initialize (sets up default configuration)
gcloud init

# Follow prompts:
# 1. Login with Google account
# 2. Select project: de-zoomcamp-412345
# 3. Set default region: us-central1
```

### **11.10 Enabling Required APIs**

**Why Enable APIs?**

```
GCP services are disabled by default.
You must explicitly enable each API you want to use.

This:
✅ Improves security
✅ Helps with cost management
✅ Shows you exactly what services are in use
```

**APIs Needed for This Course:**

**1. Navigate to APIs & Services:**

```
Console → Navigation Menu → APIs & Services → Library
```

**2. Enable These APIs:**

**Compute Engine API:**

```
Search: "Compute Engine API"
Click on result
Click "Enable"

Allows: Creating VMs, managing compute resources
```

**Cloud Storage API:**

```
Search: "Cloud Storage"
Click "Google Cloud Storage JSON API"
Click "Enable"

Allows: Creating buckets, uploading/downloading files
```

**BigQuery API:**

```
Search: "BigQuery API"
Click on result
Click "Enable"

Allows: Creating datasets, running queries, managing tables
```

**IAM Service Account Credentials API:**

```
Search: "IAM Service Account Credentials API"
Click on result
Click "Enable"

Allows: Service account impersonation, token generation
```

**Identity and Access Management (IAM) API:**

```
Search: "Identity and Access Management (IAM) API"
Click on result
Click "Enable"

Allows: Managing IAM policies, service accounts
```

**Enable via gcloud (Alternative):**

```bash
# Set project
PROJECT_ID="de-zoomcamp-412345"
gcloud config set project $PROJECT_ID

# Enable all required APIs
gcloud services enable compute.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable iamcredentials.googleapis.com

# List enabled services
gcloud services list --enabled
```

### **11.11 Testing GCP Setup**

**Test 1: List Projects**

```bash
gcloud projects list
```

**Expected Output:**

```
PROJECT_ID              NAME                      PROJECT_NUMBER
de-zoomcamp-412345      data-engineering-zoomcamp 123456789012
```

**Test 2: Create Test Bucket**

```bash
# Set variables
PROJECT_ID="de-zoomcamp-412345"
BUCKET_NAME="${PROJECT_ID}-test"

# Create bucket
gsutil mb -p $PROJECT_ID -l us-central1 gs://$BUCKET_NAME

# List buckets
gsutil ls

# Expected: gs://de-zoomcamp-412345-test/
```

**Test 3: Upload File**

```bash
# Create test file
echo "Hello GCP" > test.txt

# Upload to bucket
gsutil cp test.txt gs://$BUCKET_NAME/

# List bucket contents
gsutil ls gs://$BUCKET_NAME/

# Download file
gsutil cp gs://$BUCKET_NAME/test.txt test-downloaded.txt

# Verify
cat test-downloaded.txt
```

**Test 4: Create BigQuery Dataset**

```bash
# Create dataset
bq mk --dataset ${PROJECT_ID}:test_dataset

# List datasets
bq ls

# Expected output showing test_dataset
```

**Test 5: Run BigQuery Query**

```bash
# Run simple query
bq query --use_legacy_sql=false \
'SELECT "Hello BigQuery" AS message'

# Expected output:
# +----------------+
# |    message     |
# +----------------+
# | Hello BigQuery |
# +----------------+
```

**Cleanup Test Resources:**

```bash
# Delete bucket
gsutil rm -r gs://$BUCKET_NAME

# Delete dataset
bq rm -r -f ${PROJECT_ID}:test_dataset

# Remove test files
rm test.txt test-downloaded.txt
```

### **11.12 GCP Console Navigation**

**Key Sections:**

**Dashboard:**

```
Overview of project
- Active resources
- Billing info
- Recent activity
- Quick actions
```

**Navigation Menu (☰):**

```
Compute:
  - Compute Engine (VMs)
  - Kubernetes Engine
  - Cloud Run

Storage:
  - Cloud Storage (buckets)
  - Filestore
  - Persistent Disks

Databases:
  - Cloud SQL
  - Firestore
  - Bigtable

Analytics:
  - BigQuery
  - Dataflow
  - Pub/Sub
  - Dataproc

IAM & Admin:
  - IAM
  - Service Accounts
  - Quotas

Billing:
  - Overview
  - Budgets & Alerts
  - Cost Table
```

**Search Bar:**

```
Fastest way to navigate!

Examples:
- Type "BigQuery" → Jump to BigQuery
- Type "Storage" → Jump to Cloud Storage
- Type "IAM" → Jump to IAM & Admin
```

### **11.13 Understanding GCP Costs**

**Pricing Model:**

```
Pay-as-you-go:
- Only pay for what you use
- No upfront costs
- No termination fees

Free Tier:
- Always free products (limited usage)
- 12-month $300 credit for new accounts
```

**Services We'll Use and Their Costs:**

**Cloud Storage:**

```
Standard Storage:
  - $0.020 per GB/month (US regions)
  - First 5GB: Free (always)
  
Operations:
  - Class A (write): $0.05 per 10,000 operations
  - Class B (read): $0.004 per 10,000 operations
  
Network:
  - Egress (download): $0.12/GB (after 1GB/month free)
  - Ingress (upload): Free
```

**BigQuery:**

```
Storage:
  - Active: $0.020 per GB/month
  - Long-term (90+ days): $0.010 per GB/month
  - First 10GB: Free (always)
  
Queries:
  - On-demand: $5 per TB scanned
  - First 1TB/month: Free
  
Streaming Inserts:
  - $0.010 per 200MB
```

**Compute Engine:**

```
VMs (varies by machine type):
  - n1-standard-1: ~$0.0475/hour
  - e2-micro: Free tier (1 VM/month in US regions)
  
Storage:
  - Standard persistent disk: $0.040/GB/month
  - First 30GB: Free
```

**Cost Management Tips:**

```
✅ Set up billing alerts
✅ Use Budget alerts ($50, $100 thresholds)
✅ Delete unused resources
✅ Use Terraform destroy after testing
✅ Monitor costs daily during learning
✅ Use smallest machine types for testing
✅ Stop VMs when not in use
```

**Set Up Billing Alert:**

```
1. Navigation Menu → Billing → Budgets & Alerts
2. Create Budget
3. Name: "Learning Budget"
4. Budget Amount: $10/month
5. Alert Thresholds: 50%, 90%, 100%
6. Add your email for notifications
7. Save
```

---

## 🏗️ **Part 12: Terraform - Infrastructure as Code**

### **12.1 What is Terraform?**

**Core Definition:**

```
Terraform is an infrastructure as code (IaC) tool that 
lets you define both cloud and on-prem resources in 
human-readable configuration files that you can version, 
reuse, and share.

Created by: HashiCorp
Written in: Go
Configuration Language: HCL (HashiCorp Configuration Language)
```

**Visual Concept:**

```
Traditional Approach (Manual):
┌────────────────────────────────────┐
│  1. Log into GCP Console          │
│  2. Click "Create Bucket"          │
│  3. Fill out form                  │
│  4. Click "Create"                 │
│  5. Repeat for each resource       │
│  6. Hope you remember everything   │
└────────────────────────────────────┘
Problems:
❌ Time-consuming
❌ Error-prone
❌ Not reproducible
❌ Hard to track changes
❌ Difficult to replicate environments

Terraform Approach (IaC):
┌────────────────────────────────────┐
│  1. Write configuration file       │
│  2. Run `terraform apply`          │
│  3. All resources created          │
│  4. Version controlled             │
│  5. Easily reproducible            │
└────────────────────────────────────┘
Benefits:
✅ Fast and efficient
✅ Consistent and reliable
✅ Version controlled
✅ Repeatable deployments
✅ Easy collaboration
✅ Infrastructure as code
```

### **12.2 Why Use Terraform?**

**Key Benefits:**

**1. Simplicity:**

```
Define infrastructure in a readable configuration file
See all resources in one place
Easy to understand and modify
```

**2. Version Control:**

```
Track changes over time with Git
Review infrastructure changes like code
Collaborate with team members
Roll back to previous versions if needed
```

**3. Reproducibility:**

```
Create identical environments:
- Development
- Staging
- Production

Share infrastructure with:
- Team members
- Open source community
- Across projects
```

**4. Resource Management:**

```
Easy cleanup:
- terraform destroy removes ALL resources
- No orphaned resources
- No surprise charges
- Clean slate for testing
```

**5. Multi-Cloud:**

```
Terraform supports many providers:
✅ Google Cloud Platform (GCP)
✅ Amazon Web Services (AWS)
✅ Microsoft Azure
✅ Kubernetes
✅ 1000+ other providers
```

### **12.3 What Terraform is NOT**

**Important Limitations:**

**1. Not a Configuration Management Tool:**

```
❌ Does NOT manage software on servers
❌ Does NOT update applications
❌ Does NOT configure operating systems

For those, use:
✅ Ansible
✅ Chef
✅ Puppet
✅ SaltStack
```

**2. Cannot Change Immutable Resources:**

```
Some resources can't be modified in-place:
- VM machine type (must recreate)
- Bucket location (must recreate)
- BigQuery dataset location (must recreate)

Terraform will:
1. Destroy old resource
2. Create new resource with new settings
```

**3. Only Manages Terraform-Defined Resources:**

```
If you create resources outside Terraform:
- Terraform doesn't know about them
- Terraform won't manage them
- Terraform won't destroy them

Solution: Define ALL infrastructure in Terraform
```

**4. Not for Application Deployment:**

```
Terraform creates infrastructure, not applications.

Wrong Use:
❌ Deploying Docker containers to production
❌ Updating application code
❌ Managing application configuration

Right Use:
✅ Creating GKE cluster for containers
✅ Setting up VMs for applications
✅ Provisioning databases
```

### **12.4 How Terraform Works**

**Architecture:**

```
┌─────────────────────────────────────────────────────┐
│               Terraform Workflow                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Local Machine                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ 1. Write Configuration (.tf files)           │  │
│  │    - Define providers (GCP, AWS, etc.)       │  │
│  │    - Define resources (buckets, VMs)         │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                              │
│  ┌──────────────────────────────────────────────┐  │
│  │ 2. terraform init                            │  │
│  │    - Downloads provider plugins              │  │
│  │    - Initializes backend                     │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                              │
│  ┌──────────────────────────────────────────────┐  │
│  │ 3. terraform plan                            │  │
│  │    - Preview changes                         │  │
│  │    - Show what will be created/modified      │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                              │
│  ┌──────────────────────────────────────────────┐  │
│  │ 4. terraform apply                           │  │
│  │    - Create/modify resources                 │  │
│  │    - Update state file                       │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                              │
│  ┌──────────────────────────────────────────────┐  │
│  │             Cloud Provider (GCP)             │  │
│  │  ┌────────────┐  ┌────────────┐              │  │
│  │  │  Bucket    │  │  BigQuery  │              │  │
│  │  └────────────┘  └────────────┘              │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**State File:**

```
terraform.tfstate is crucial!

What it contains:
- Current infrastructure state
- Resource IDs
- Resource attributes
- Dependencies between resources

Why it matters:
✅ Terraform compares desired state (config files) 
   with current state (state file)
✅ Determines what changes to make
✅ Tracks resource metadata
✅ Maps config to real resources

⚠️ Never manually edit state file!
⚠️ Backup state file regularly
⚠️ Use remote state for teams
```

### **12.5 Terraform Providers**

**What is a Provider?**

```
A provider is a plugin that allows Terraform to interact 
with an API.

Think of it as a translator:
- You write HCL (Terraform language)
- Provider translates to API calls
- Cloud provider understands API calls
```

**Common Providers:**

```
Cloud Providers:
- google (GCP)
- aws (Amazon Web Services)
- azurerm (Microsoft Azure)
- digitalocean

Container Orchestration:
- kubernetes
- helm
- docker

Other:
- github
- datadog
- postgresql
- random
```

**Provider Configuration Example:**

````hcl
# Configure the Google Cloud provider
provider "google" {
  project     = "de-zoomcamp-412345"
  region      = "us-central1"
  credentials = file("~/.gc/ny-rides.json")
}
````

### **12.6 Installing Terraform**

**Linux (Ubuntu/Debian):**

```bash
# Add HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | \
sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Add HashiCorp repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list

# Update and install
sudo apt update && sudo apt install terraform

# Verify installation
terraform version
```

**macOS (Homebrew):**

```bash
# Install via Homebrew
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Verify
terraform version
```

**Windows:**

```
Option 1: Chocolatey
choco install terraform

Option 2: Manual Installation
1. Download from: https://www.terraform.io/downloads
2. Extract terraform.exe
3. Add to PATH
4. Verify: terraform version
```

**Verify Installation:**

```bash
terraform version

# Expected output:
# Terraform v1.7.0
# on linux_amd64
```

### **12.7 Essential Terraform Commands**

**Command Reference:**

**`terraform init`:**

```bash
# Initialize Terraform directory
terraform init

What it does:
✅ Downloads provider plugins
✅ Initializes backend
✅ Prepares working directory
✅ Creates .terraform directory

When to use:
- First time in new Terraform directory
- After adding new providers
- After changing backend configuration
```

**`terraform fmt`:**

```bash
# Format Terraform files
terraform fmt

What it does:
✅ Formats .tf files to canonical style
✅ Fixes indentation
✅ Aligns assignments
✅ Sorts arguments

When to use:
- Before committing code
- After editing files
- To maintain consistency
```

**`terraform validate`:**

```bash
# Validate configuration
terraform validate

What it does:
✅ Checks syntax errors
✅ Validates attribute names
✅ Checks for required arguments
✅ Does NOT check provider API

When to use:
- After writing/editing config
- Before plan/apply
- In CI/CD pipelines
```

**`terraform plan`:**

```bash
# Preview changes
terraform plan

What it does:
✅ Shows what Terraform will do
✅ Compares config to state
✅ Displays proposed changes
✅ Does NOT make changes

Output symbols:
  + create
  - destroy
  ~ update in-place
  -/+ destroy and recreate

When to use:
- Before applying changes
- To review proposed changes
- To catch mistakes
```

**`terraform apply`:**

```bash
# Apply changes
terraform apply

# Auto-approve (skip confirmation)
terraform apply -auto-approve

What it does:
✅ Creates/updates/deletes resources
✅ Updates state file
✅ Outputs result

When to use:
- After reviewing plan
- When ready to deploy
- After confirming changes
```

**`terraform destroy`:**

```bash
# Destroy all resources
terraform destroy

# Auto-approve (dangerous!)
terraform destroy -auto-approve

What it does:
✅ Destroys ALL resources defined in config
✅ Updates state file
✅ Removes infrastructure

⚠️ Warning:
- Cannot be undone
- Will delete data
- Will stop running services

When to use:
- Cleanup after testing
- Tear down environments
- Cost management
```

**`terraform show`:**

```bash
# Show current state
terraform show

What it does:
✅ Displays current state
✅ Shows resource details
✅ Human-readable output

When to use:
- Check current infrastructure
- Debug issues
- Verify deployments
```

**`terraform output`:**

```bash
# Show outputs
terraform output

# Show specific output
terraform output bucket_name

What it does:
✅ Displays output values
✅ Useful for getting resource info
✅ Can be used in scripts

When to use:
- Get resource details
- Pass info to other tools
- Debugging
```

I'll continue with the Terraform practical implementation.

---

### **12.8 Terraform File Structure**

**Typical Project Structure:**

```
terraform/
├── main.tf           # Main configuration
├── variables.tf      # Variable definitions
├── outputs.tf        # Output definitions
├── terraform.tfvars  # Variable values (gitignored!)
├── .terraform/       # Provider plugins (generated)
├── .terraform.lock.hcl  # Provider version lock
├── terraform.tfstate    # Current state (gitignored!)
└── terraform.tfstate.backup  # State backup
```

**File Purposes:**

| File | Purpose | Commit to Git? |
|------|---------|----------------|
| `main.tf` | Resource definitions | ✅ Yes |
| `variables.tf` | Variable declarations | ✅ Yes |
| `outputs.tf` | Output definitions | ✅ Yes |
| `terraform.tfvars` | Variable values (may contain secrets) | ❌ No |
| `.terraform/` | Downloaded plugins | ❌ No |
| `*.tfstate` | State files (contain sensitive data) | ❌ No |

### **12.9 Creating Your First Terraform Configuration**

**Navigate to Terraform Directory:**

```bash
# Create terraform directory in your project
cd ~/data-engineering-zoomcamp
mkdir terraform
cd terraform
```

**Create main.tf:**

````hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  project = "de-zoomcamp-412345"  # Replace with your project ID
  region  = "us-central1"
}

# Create a GCS bucket for data lake
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "de-zoomcamp-412345-terra-bucket"  # Must be globally unique
  location      = "US"
  force_destroy = true

  # Lifecycle rule - delete files older than 30 days
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  # Abort incomplete multipart uploads after 1 day
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# Create BigQuery dataset
resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "demo_dataset"
  location   = "US"
}
````

**Explanation of main.tf:**

**1. Terraform Block:**

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}
```

- Declares required providers
- Specifies provider version for consistency
- `source`: Where to download provider from

**2. Provider Block:**

```hcl
provider "google" {
  project = "de-zoomcamp-412345"
  region  = "us-central1"
}
```

- Configures the Google Cloud provider
- Sets default project and region
- Credentials from `GOOGLE_APPLICATION_CREDENTIALS` env var

**3. Resource Blocks:**

```hcl
resource "google_storage_bucket" "data_lake_bucket" {
  # Configuration
}
```

- `resource`: Keyword to define a resource
- `"google_storage_bucket"`: Resource type
- `"data_lake_bucket"`: Resource name (local to Terraform)

### **12.10 Parameterizing with Variables**

**Create variables.tf:**

````hcl
variable "project" {
  description = "Your GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for GCP resources"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "Location for multi-regional resources"
  type        = string
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  type        = string
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "GCS Bucket Name"
  type        = string
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  type        = string
  default     = "STANDARD"
}
````

**Update main.tf to Use Variables:**

````hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "data_lake_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
````

**Create terraform.tfvars (Contains Your Values):**

````hcl
project          = "de-zoomcamp-412345"  # Replace with YOUR project ID
gcs_bucket_name  = "de-zoomcamp-412345-terra-bucket"  # Must be globally unique
````

**⚠️ Security: Add to .gitignore:**

```bash
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Exclude all .tfvars files (may contain sensitive data)
*.tfvars
*.tfvars.json

# Ignore override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Ignore CLI configuration files
.terraformrc
terraform.rc

# Credentials
*.json
```

**Why Use Variables?**

```
✅ Reusability: Same config for different projects
✅ Flexibility: Easy to change values
✅ Security: Separate config from secrets
✅ Collaboration: Share templates, customize values
```

### **12.11 Adding Outputs**

**Create outputs.tf:**

````hcl
output "gcs_bucket_name" {
  description = "GCS Bucket Name"
  value       = google_storage_bucket.data_lake_bucket.name
}

output "gcs_bucket_url" {
  description = "GCS Bucket URL"
  value       = google_storage_bucket.data_lake_bucket.url
}

output "bigquery_dataset_id" {
  description = "BigQuery Dataset ID"
  value       = google_bigquery_dataset.demo_dataset.dataset_id
}
````

**Why Use Outputs?**

```
✅ Display important information after apply
✅ Use in scripts or other tools
✅ Document what was created
✅ Pass to other Terraform modules
```

### **12.12 Running Terraform**

**Step-by-Step Execution:**

**1. Set Up Authentication:**

```bash
# Ensure you have service account key
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gc/ny-rides.json"

# Verify
echo $GOOGLE_APPLICATION_CREDENTIALS
```

**2. Initialize Terraform:**

```bash
cd terraform

# Initialize
terraform init
```

**Expected Output:**

```
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/google versions matching "5.13.0"...
- Installing hashicorp/google v5.13.0...
- Installed hashicorp/google v5.13.0

Terraform has been successfully initialized!
```

**What Happened:**

- Downloaded Google provider plugin
- Created `.terraform/` directory
- Created `.terraform.lock.hcl` lock file

**3. Format Configuration:**

```bash
terraform fmt
```

**4. Validate Configuration:**

```bash
terraform validate
```

**Expected Output:**

```
Success! The configuration is valid.
```

**5. Preview Changes:**

```bash
terraform plan
```

**Expected Output:**

```
Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + id                         = (known after apply)
      + location                   = "US"
      + project                    = "de-zoomcamp-412345"
    }

  # google_storage_bucket.data_lake_bucket will be created
  + resource "google_storage_bucket" "data_lake_bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "de-zoomcamp-412345-terra-bucket"
      + project                     = (known after apply)
      + storage_class               = "STANDARD"
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "Delete"
            }
          + condition {
              + age                   = 30
            }
        }

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

**Understanding the Output:**

```
Symbol meanings:
  + create
  - destroy
  ~ update in-place
  -/+ destroy and recreate
  
(known after apply) = Value determined during creation
```

**6. Apply Configuration:**

```bash
terraform apply
```

**You'll be prompted:**

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: 
```

**Type `yes` and press Enter.**

**Expected Output:**

```
google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.data_lake_bucket: Creating...
google_storage_bucket.data_lake_bucket: Creation complete after 2s
google_bigquery_dataset.demo_dataset: Creation complete after 1s

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

bigquery_dataset_id = "demo_dataset"
gcs_bucket_name = "de-zoomcamp-412345-terra-bucket"
gcs_bucket_url = "gs://de-zoomcamp-412345-terra-bucket"
```

**7. Verify in GCP Console:**

**Cloud Storage:**

```
Navigate to: Cloud Storage → Buckets
You should see: de-zoomcamp-412345-terra-bucket
```

**BigQuery:**

```
Navigate to: BigQuery
You should see: demo_dataset
```

**8. View Outputs:**

```bash
# Show all outputs
terraform output

# Show specific outputcommand 'claude-vscode.editor.openLast' not found
terraform output gcs_bucket_name
```

**9. Inspect State:**

```bash
# Show current state
terraform show

# List resources in state
terraform state list
```

**10. Make Changes:**

Let's modify our configuration:

````hcl
# Add a new variable value
bq_dataset_name = "taxi_data"  # Change dataset name
````

**Run Plan to See Changes:**

```bash
terraform plan
```

**Output:**

```
  # google_bigquery_dataset.demo_dataset must be replaced
-/+ resource "google_bigquery_dataset" "demo_dataset" {
      ~ dataset_id                 = "demo_dataset" -> "taxi_data" # forces replacement
      ~ id                         = "projects/.../datasets/demo_dataset" -> (known after apply)
        # ...
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

**Why `-/+` (destroy and recreate)?**

```
BigQuery dataset ID is immutable.
Cannot be changed in-place.
Must destroy old and create new.
```

**Apply Changes:**

```bash
terraform apply
# Type 'yes' when prompted
```

**11. Destroy Resources:**

```bash
terraform destroy
```

**Prompt:**

```
Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value:
```

**Type `yes` to confirm.**

**Expected Output:**

```
google_bigquery_dataset.demo_dataset: Destroying...
google_storage_bucket.data_lake_bucket: Destroying...
google_storage_bucket.data_lake_bucket: Destruction complete after 1s
google_bigquery_dataset.demo_dataset: Destruction complete after 2s

Destroy complete! Resources: 2 destroyed.
```

**Verify Cleanup:**

```
GCP Console → Cloud Storage → No bucket
GCP Console → BigQuery → No dataset
```

### **12.13 Advanced Terraform Features**

**Using Functions:**

````hcl
locals {
  # Local values (computed once)
  bucket_name = "${var.project}-${var.region}-data-lake"
  
  # Generate random suffix
  random_suffix = random_id.bucket_suffix.hex
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${local.bucket_name}-${local.random_suffix}"
  location      = var.location
  storage_class = var.gcs_storage_class
  force_destroy = true
}
````

**Conditional Resources:**

````hcl
variable "create_bucket" {
  description = "Whether to create the bucket"
  type        = bool
  default     = true
}

resource "google_storage_bucket" "data_lake_bucket" {
  count = var.create_bucket ? 1 : 0
  
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
}
````

**For Each (Multiple Similar Resources):**

````hcl
variable "datasets" {
  description = "BigQuery datasets to create"
  type        = set(string)
  default     = ["raw_data", "staging", "production"]
}

resource "google_bigquery_dataset" "datasets" {
  for_each = var.datasets
  
  dataset_id = each.value
  location   = var.location
}
````

### **12.14 Terraform Best Practices**

**1. Version Control:**

```bash
# Always use Git
git init
git add main.tf variables.tf outputs.tf .gitignore
git commit -m "Initial Terraform configuration"
```

**2. State Management:**

```
For Teams:
✅ Use remote state (GCS bucket)
✅ Enable state locking
✅ Never commit state files

Configuration:
```

````hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "terraform/state"
  }
}
````

**3. Workspace Usage:**

```bash
# Create workspaces for environments
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch workspace
terraform workspace select dev

# List workspaces
terraform workspace list
```

**4. Module Organization:**

```
For Larger Projects:

terraform/
├── modules/
│   ├── storage/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── bigquery/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
└── README.md
```

**5. Security Best Practices:**

```
✅ Never commit credentials
✅ Use environment variables
✅ Encrypt state files
✅ Use service accounts with minimal permissions
✅ Enable audit logging
✅ Regular security reviews
```

**6. Code Quality:**

```bash
# Always format
terraform fmt -recursive

# Always validate
terraform validate

# Use pre-commit hooks
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
```

### **12.15 Troubleshooting Common Issues**

**Issue 1: Authentication Failed**

```
Error: google: could not find default credentials

Solution:
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gc/ny-rides.json"
```

**Issue 2: Resource Already Exists**

```
Error: Error creating Dataset: googleapi: Error 409: Already Exists

Solution:
terraform import google_bigquery_dataset.demo_dataset projects/PROJECT_ID/datasets/DATASET_ID
```

**Issue 3: Permission Denied**

```
Error: Error creating bucket: googleapi: Error 403: Forbidden

Solution:
1. Check service account has correct roles
2. Verify APIs are enabled
3. Check project ID is correct
```

**Issue 4: State Lock**

```
Error: Error locking state: state locked

Solution:
terraform force-unlock LOCK_ID
```

**Issue 5: Provider Version Conflict**

```
Error: Failed to query available provider packages

Solution:
rm -rf .terraform .terraform.lock.hcl
terraform init
```

---

## 📝 **Summary and Next Steps**

### **What We've Accomplished**

**Module 1 Complete:**

```
✅ Docker fundamentals and containerization
✅ Python virtual environments with uv
✅ Data pipeline development
✅ PostgreSQL in Docker
✅ Data ingestion from NYC Taxi dataset
✅ Docker Compose for multi-container apps
✅ SQL refresher and data querying
✅ GCP account setup and configuration
✅ Terraform infrastructure as code
✅ Complete local and cloud data engineering setup
```

### **Key Takeaways**

**Docker:**

```
- Containers provide isolated, reproducible environments
- Volume mapping persists data
- Docker Compose orchestrates multiple containers
- Essential for modern data engineering
```

**Python & Data Engineering:**

```
- uv for fast dependency management
- Pandas for data transformation
- SQLAlchemy for database interaction
- Click for CLI applications
```

**Databases:**

```
- PostgreSQL for structured data
- pgAdmin for database management
- SQL for data analysis and transformation
- Proper schema design matters
```

**Cloud Infrastructure:**

```
- GCP provides scalable cloud resources
- Service accounts for secure authentication
- BigQuery for data warehousing
- Cloud Storage for data lakes
```

**Infrastructure as Code:**

```
- Terraform defines infrastructure declaratively
- Version control for infrastructure
- Reproducible deployments
- Easy cleanup and cost management
```

### **Next Steps**

**Continue the Course:**

```
Module 2: Workflow Orchestration
- Apache Airflow or Prefect
- DAGs and task dependencies
- Scheduling and monitoring
- Error handling and retries

Module 3: Data Warehouse
- BigQuery in depth
- Partitioning and clustering
- Cost optimization
- Best practices

Module 4: Analytics Engineering
- dbt (data build tool)
- Data modeling
- Testing and documentation
- CI/CD for analytics

Module 5: Batch Processing
- Apache Spark
- Distributed computing
- Processing large datasets
- Performance optimization

Module 6: Streaming
- Apache Kafka
- Real-time data processing
- Stream processing with Spark
```

**Practice Projects:**

```
1. Build end-to-end pipeline:
   - Ingest data from API
   - Store in Cloud Storage
   - Process with Pandas/Spark
   - Load into BigQuery
   - Deploy with Terraform

2. Automate with Airflow:
   - Schedule daily data loads
   - Add data quality checks
   - Send alerts on failures

3. Create analytics:
   - Build dbt models
   - Create dashboards
   - Share insights
```

**Resources:**

```
Official Documentation:
- Docker: https://docs.docker.com/
- Terraform: https://www.terraform.io/docs
- GCP: https://cloud.google.com/docs
- PostgreSQL: https://www.postgresql.org/docs/

Community:
- Data Engineering Zoomcamp Slack
- Stack Overflow
- Reddit r/dataengineering
- GitHub repositories
```

---

**Congratulations! 🎉**

You've completed Module 1 of the Data Engineering Zoomcamp! You now have:

- ✅ A solid foundation in Docker and containerization
- ✅ Hands-on experience with data pipelines
- ✅ Cloud infrastructure setup with GCP
- ✅ Infrastructure as code skills with Terraform
- ✅ SQL knowledge for data analysis
- ✅ Tools and environment for the rest of the course

**Keep learning, keep building, and happy data engineering!** 🚀📊