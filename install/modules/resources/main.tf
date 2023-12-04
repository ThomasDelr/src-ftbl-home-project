resource "google_storage_bucket" "gcp_bucket_src_ftbl" {
  name          = var.google_bucket_name
  project = var.google_project_id
  location      = "EU"
  force_destroy = true
  storage_class = "STANDARD"
  public_access_prevention = "enforced"
}

resource "google_storage_bucket" "gcp_bucket_src_ftbl_processed" {
  name          = var.google_bucket_name_processed
  project = var.google_project_id
  location      = "EU"
  force_destroy = true
  storage_class = "STANDARD"
  public_access_prevention = "enforced"
}
