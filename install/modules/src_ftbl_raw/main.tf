resource "google_bigquery_dataset" "raw_src_ftbl_dataset" {
  project = var.google_project_id
  dataset_id         = "src_ftbl_raw"
  friendly_name               = "src ftbl raw dataset"
  description                 = "This is a dataset containing skills corner data from src ftbl"
  location                    = "EU"
  labels = {"env"="dev",
            "use"="storage"}
}



resource "google_bigquery_table" "raw_src_ftbl_tracking" {
  project = var.google_project_id
  dataset_id = google_bigquery_dataset.raw_src_ftbl_dataset.dataset_id
  table_id = "tracking"
  deletion_protection=false

  labels = {
    env="dev"
    use="raw"
  }
  schema = file("../schema/raw_tracking.json")
}

resource "google_bigquery_table" "raw_src_ftbl_metadata" {
  project = var.google_project_id
  dataset_id = google_bigquery_dataset.raw_src_ftbl_dataset.dataset_id
  table_id = "metadata"
  deletion_protection=false

  labels = {
    env="dev"
    use="raw"
  }
  schema = file("../schema/raw_metadata.json")
}