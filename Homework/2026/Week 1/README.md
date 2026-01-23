# Week 1 Summary: Docker, SQL & Terraform

## What I Learned in Week 1

### 🐳 Docker Fundamentals
- **Containerization concepts**: Images vs containers, stateless by default
- **Docker volumes** for persistent data storage
- **Docker networking** for container-to-container communication
- **Building custom Docker images** using Dockerfiles
- **Docker Compose** for orchestrating multi-container applications

---

### 🐍 Python Development
- **Virtual environments** using **UV** (modern, fast package manager)
- **Data pipeline structure**: Extract → Transform → Load (ETL)
- **CLI development** using Click for parameterized scripts
- **Pandas** for data processing and chunked CSV reading
- **SQLAlchemy** for database connectivity

---

### 🗄️ PostgreSQL & Database Management
- **Running PostgreSQL in Docker** with environment variables and volumes
- **pgcli** for command-line database access
- **pgAdmin** for GUI-based database management
- **Database connectivity** from both host and container contexts
- **Data ingestion** from CSV to PostgreSQL in chunks

---

### 📊 SQL Essentials
- **Basic queries**: SELECT, WHERE, LIMIT
- **Aggregations**: COUNT, SUM, AVG, MAX, MIN
- **Grouping and filtering**: GROUP BY, HAVING
- **Joins**: INNER JOIN for combining tables
- **Practical analysis** on NYC Taxi dataset

---

### ☁️ Cloud Infrastructure (GCP)
- **Google Cloud Platform basics**: Projects, buckets, datasets
- **Cloud Storage** for object storage
- **BigQuery** as a cloud data warehouse
- **Service accounts** for programmatic access
- **IAM roles** for access control

---

### 🌍 Infrastructure as Code (Terraform)
- **Terraform fundamentals**: Declarative infrastructure management
- **Provider configuration** for GCP
- **Resource definitions**: Storage buckets, BigQuery datasets
- **Terraform workflow**: init → plan → apply → destroy
- **Version control** for infrastructure code

---

### 🛠️ Best Practices
- ✅ Use `.gitignore` for credentials and generated files
- ✅ Explicit schema definitions for data ingestion
- ✅ Chunked processing for large datasets
- ✅ Named volumes for data persistence
- ✅ Docker networks for service isolation
- ✅ Always clean up cloud resources to avoid charges

---

### 🎯 Real-World Skills Gained
- Built a **complete data ingestion pipeline**
- Containerized applications for **reproducibility**
- Managed databases with **Docker and SQL**
- Provisioned cloud infrastructure with **code**
- Orchestrated multi-service applications with **Docker Compose**

---

