terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  credentials = file("${path.module}/keys/my-creds.json")
  project     = var.project
  region      = var.region
}

# GCS Bucket for homework
resource "google_storage_bucket" "homework_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
}

# BigQuery Dataset for homework
resource "google_bigquery_dataset" "homework_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
  
  delete_contents_on_destroy = true
}
