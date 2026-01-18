variable "project" {
  description = "GCP Project ID"
  default     = "de-zoomcamp-2025-12345"
}

variable "region" {
  description = "GCP Region"
  default     = "europe-west2"
}

variable "location" {
  description = "Multi-region location"
  default     = "EU"
}

variable "gcs_bucket_name" {
  description = "GCS Bucket Name"
  default     = "de-zoomcamp-2025-homework-bucket"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "homework_dataset"
}