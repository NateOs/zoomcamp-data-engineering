provider "google" {
	project = "scenic-healer-416216"
	region  = "us-central1"
	credentials = file("/keys/my_creds.json")
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraterra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}