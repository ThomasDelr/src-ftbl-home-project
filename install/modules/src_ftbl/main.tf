resource "google_bigquery_dataset" "raw_src_ftbl_dataset" {
  project = var.google_project_id
  dataset_id         = "src_ftbl"
  friendly_name               = "src ftbl  dataset"
  description                 = "This is a dataset containing skills corner data from src ftbl"
  location                    = "EU"
  labels = {"env"="dev",
            "use"="analytics"}
}

