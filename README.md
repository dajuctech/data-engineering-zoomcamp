# data-engineering-zoomcamp

Data Engineering Zoomcamp - Learning Journey

## Week 1: Introduction to Data Engineering

## Docker and PostgreSQL Workshop

Learned how to:
- Set up a data ingestion pipeline using Python and Docker
- Use Docker Compose to orchestrate PostgreSQL and pgAdmin containers
- Ingest CSV data into PostgreSQL in chunks using pandas and SQLAlchemy
- Manage Python dependencies with UV in a containerized environment
- Create reproducible data pipelines with multi-stage Docker builds

### SQL Refresher Workshop (1.2.6)
Learned how to:
- Join tables using implicit (WHERE) and explicit (JOIN) syntax
- Use INNER JOIN, LEFT JOIN, RIGHT JOIN, and OUTER JOIN
- Check for missing data with NOT IN and IS NULL
- Aggregate data using GROUP BY with COUNT, MAX, and other functions
- Order results with ORDER BY (ASC/DESC)
- Combine location data from zones table with taxi trip data
- Write complex SQL queries for data analysis and reporting

### Google Cloud Platform Setup (1.2.7)
Learned how to:
- Set up a GCP account with $300 free trial credits
- Create and configure a GCP project for data engineering workloads
- Set up service accounts with proper IAM roles (Storage Admin, BigQuery Admin)
- Configure Google Cloud SDK authentication using service account JSON keys
- Create and manage Cloud Storage buckets with regional configuration
- Upload datasets to Cloud Storage using `gsutil` CLI commands and GUI frontend
- Run SQL queries in BigQuery Console GUI for data analysis
- Work with environment variables for secure credential management
- Navigate GCP Console for Cloud Storage and BigQuery operations

### Terraform Infrastructure as Code (1.3.1)
Learned how to:
- Install and configure Terraform for infrastructure provisioning
- Understand Infrastructure as Code (IaC) principles and benefits
- Define cloud resources in declarative `.tf` configuration files
- Use Terraform providers to communicate with GCP APIs
- Separate configuration into `main.tf`, `variables.tf`, and `outputs.tf` files
- Declare and reference variables across Terraform files using `var.variable_name`
- Initialize Terraform projects with `terraform init` to download provider plugins
- Preview infrastructure changes with `terraform plan` before applying
- Provision GCP resources (Cloud Storage buckets, BigQuery datasets) with `terraform apply`
- Manage infrastructure state with `.tfstate` files
- Destroy all managed resources cleanly with `terraform destroy`
- Secure sensitive files using `.gitignore` for credentials and state files
- Configure bucket lifecycle rules for automatic data deletion
- Set up multi-region storage locations for high availability

**Skills Acquired:**
- Terraform CLI workflow (`init`, `plan`, `apply`, `destroy`, `fmt`, `validate`)
- Writing HCL (HashiCorp Configuration Language) syntax
- Managing GCP resources programmatically via Terraform
- Version controlling infrastructure configurations
- Implementing reproducible infrastructure deployments
- Separating configuration from implementation using variables
- Securing credentials in Terraform projects
- Understanding immutable infrastructure concepts

**Key Terraform Commands:**
```bash
terraform init      # Initialize and download providers
terraform fmt       # Format code to standard style
terraform validate  # Check syntax and configuration
terraform plan      # Preview changes before applying
terraform apply     # Create/update infrastructure
terraform destroy   # Remove all managed resources
terraform show      # Display current state
terraform output    # Show output values
