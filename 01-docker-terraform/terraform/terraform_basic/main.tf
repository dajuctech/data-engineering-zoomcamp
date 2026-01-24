terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  credentials = file("./keys/my-creds.json")
  project     = "my-project-id"
  region      = "us-central1"
}

# Create a simple GCS Bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "my-unique-bucket-name"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Create a BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "my_dataset"
  location   = "US"
}
