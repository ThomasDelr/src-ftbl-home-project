resource "google_bigquery_dataset" "monitoring_dataset" {
  project = var.google_project_id
  dataset_id         = "monitoring"
  friendly_name               = "src ftbl monitoring dataset"
  description                 = "This is a dataset containing monitoring data for src ftbl home project"
  location                    = "EU"
  labels = {"env"="dev",
            "use"="monitoring"}
}

resource "google_bigquery_table" "src_ftbl_game_summary" {
  project = var.google_project_id
  dataset_id = "src_monitoring"
  table_id = "step_execution"
  deletion_protection=false

  labels = {
    env="dev"
    use="monitoring"
  }
}
