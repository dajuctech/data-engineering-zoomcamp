variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "de-zoomcamp-2025-12345"
}

variable "region" {
  description = "Region for resources"
  default     = "europe-west2" # London
}

variable "location" {
  description = "Location for BigQuery/GCS (multi-region)"
  default     = "EU" # Europe multi-region
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "de-zoomcamp-2025-12345-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}