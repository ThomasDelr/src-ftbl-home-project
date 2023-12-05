provider "google" {
  project = var.google_project_id
  region  = "europe-west1"
  zone    = "europe-west9"
}

module "resources" {
    source = "./resources"
    google_bucket_name = "src-ftbl-data"
    google_bucket_name_processed = "src-ftbl-data-processed"
    google_project_id = "dev-src-ftbl-home-project"
}

module "src_ftbl_raw" {
    source = "./src_ftbl_raw"
    google_project_id = "dev-src-ftbl-home-project"
}

module "src_ftbl_staging" {
    source = "./src_ftbl_staging"
    google_project_id = "dev-src-ftbl-home-project"
}

module "src_ftbl" {
    source = "./src_ftbl"
    google_project_id = "dev-src-ftbl-home-project"
}

terraform {
  backend "gcs" {
    bucket  = "src-ftbl-tf"
    prefix  = "terraform/state"
  }
}
