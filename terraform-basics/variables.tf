variable "location" {
	description = "project location"
	default = "US"
}

variable "bq_dataset_name" {
	description = "my bigquery dataset name"
	default = "demo_dataset"
}

variable "gcs_bucket_name" {
	description = "my storage bucket name"
	default = "terraterra-bucket"
  
}

variable "project_name" {
  description = "name of google project"
  default = "scenic-healer-416216"
}

variable "region" {
	description = "region"
	default = "us-central1"
  
}