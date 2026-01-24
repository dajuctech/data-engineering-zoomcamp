# Terraform Infrastructure as Code

Terraform configurations for provisioning Google Cloud Platform (GCP) resources for data engineering workloads.

## 📁 Project Structure

```
terraform/
├── terraform_basic/
│   └── main.tf              # Simple hardcoded configuration
└── terraform_with_variables/
    ├── main.tf              # Parameterized configuration
    └── variables.tf         # Configurable variables
```

## 🎯 Resources Created

| Resource | Type | Purpose |
|----------|------|---------|
| GCS Bucket | `google_storage_bucket` | Data lake storage for raw/processed data |
| BigQuery Dataset | `google_bigquery_dataset` | Data warehouse for analytics |

## 🚀 Quick Start

### Prerequisites

1. **Install Terraform** (v1.0+)
   ```bash
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
   wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform
   
   # Verify installation
   terraform --version
   ```

2. **Set up GCP Service Account**
   - Go to [GCP Console](https://console.cloud.google.com/) → IAM & Admin → Service Accounts
   - Create a new service account with roles:
     - `Storage Admin` (for GCS bucket management)
     - `BigQuery Admin` (for BigQuery dataset management)
   - Download JSON key and save as `keys/my-creds.json`

3. **Enable GCP APIs**
   ```bash
   gcloud services enable storage.googleapis.com
   gcloud services enable bigquery.googleapis.com
   ```

### Option 1: Basic Configuration (Hardcoded)

```bash
cd terraform_basic

# Edit main.tf to update:
# - project = "your-gcp-project-id"
# - name = "your-unique-bucket-name"

terraform init      # Download provider plugins
terraform plan      # Preview changes
terraform apply     # Create resources (type 'yes' to confirm)
```

### Option 2: Variables Configuration (Recommended)

```bash
cd terraform_with_variables

# Edit variables.tf with your values OR use command-line flags

terraform init
terraform plan
terraform apply
```

## ⚙️ Configuration Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `credentials` | Path to GCP service account JSON | `./keys/my-creds.json` |
| `project` | GCP project ID | `de-zoomcamp-2025-12345` |
| `region` | GCP region for resources | `europe-west2` (London) |
| `location` | Multi-region for GCS/BigQuery | `EU` |
| `gcs_bucket_name` | Name for Cloud Storage bucket | `de-zoomcamp-2025-12345-terra-bucket` |
| `bq_dataset_name` | Name for BigQuery dataset | `demo_dataset` |
| `gcs_storage_class` | Storage class for bucket | `STANDARD` |

### Override Variables

```bash
# Using command-line flags
terraform apply -var="project=my-project" -var="gcs_bucket_name=my-bucket"

# Using a tfvars file
terraform apply -var-file="production.tfvars"
```

## 📋 Terraform Commands Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory, download providers |
| `terraform fmt` | Format code to standard style |
| `terraform validate` | Check syntax and configuration validity |
| `terraform plan` | Preview infrastructure changes |
| `terraform apply` | Create or update infrastructure |
| `terraform destroy` | Remove all managed resources |
| `terraform show` | Display current state |
| `terraform output` | Show output values |

## 🏗️ Infrastructure Details

### GCS Bucket Configuration

```hcl
resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  # Auto-delete objects after 3 days
  lifecycle_rule {
    condition { age = 3 }
    action { type = "Delete" }
  }

  # Clean up incomplete uploads after 1 day
  lifecycle_rule {
    condition { age = 1 }
    action { type = "AbortIncompleteMultipartUpload" }
  }
}
```

### BigQuery Dataset Configuration

```hcl
resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
```

## 🔐 Security Best Practices

1. **Never commit credentials** - Add to `.gitignore`:
   ```gitignore
   *.json
   keys/
   *.tfstate
   *.tfstate.*
   .terraform/
   ```

2. **Use environment variables** for sensitive data:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

3. **Use remote state** for team collaboration:
   ```hcl
   terraform {
     backend "gcs" {
       bucket = "my-terraform-state-bucket"
       prefix = "terraform/state"
     }
   }
   ```

## 🧹 Cleanup

Remove all infrastructure resources:

```bash
terraform destroy
# Type 'yes' when prompted
```

## 🔗 Related Resources

- [Terraform GCP Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [GCP Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [GCP BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Data Engineering Zoomcamp - Terraform Module](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp)
