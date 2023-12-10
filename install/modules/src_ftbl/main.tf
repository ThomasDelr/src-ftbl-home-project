resource "google_bigquery_dataset" "raw_src_ftbl_dataset" {
  project = var.google_project_id
  dataset_id         = "src_ftbl"
  friendly_name               = "src ftbl  dataset"
  description                 = "This is a dataset containing skills corner data from src ftbl"
  location                    = "EU"
  labels = {"env"="dev",
            "use"="analytics"}
}

resource "google_bigquery_table" "src_ftbl_game_summary" {
  project = var.google_project_id
  dataset_id = google_bigquery_dataset.raw_src_ftbl_dataset.dataset_id
  table_id = "game_summary"
  deletion_protection=false

  labels = {
    env="dev"
    use="analytics"
  }
  schema = file("../schema/game_summary.json")
  time_partitioning {
    type = "DAY"
    require_partition_filter = true
  }
  clustering = ['game_id', 'home_team_id', 'away_team_id']
}

resource "google_bigquery_table" "src_ftbl_game_players_summary" {
  project = var.google_project_id
  dataset_id = google_bigquery_dataset.raw_src_ftbl_dataset.dataset_id
  table_id = "game_players_summary"
  deletion_protection=false

  labels = {
    env="dev"
    use="analytics"
  }
  schema = file("../schema/game_players_summary.json")
  time_partitioning {
    type = "DAY"
    require_partition_filter = true
  }
  clustering = ['game_id', 'team_id', 'player_id']
}

resource "google_bigquery_table" "src_ftbl_game_tracking" {
  project = var.google_project_id
  dataset_id = google_bigquery_dataset.raw_src_ftbl_dataset.dataset_id
  table_id = "game_tracking"
  deletion_protection=false

  labels = {
    env="dev"
    use="analytics"
  }
  schema = file("../schema/game_tracking.json")
  time_partitioning {
    type = "DAY"
    require_partition_filter = true
  }
  clustering = ['game_id', 'team_id', 'trackable_object']
}