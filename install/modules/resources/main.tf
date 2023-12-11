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

## service account
# Grant necessary permissions to the service account
resource "google_project_iam_member" "sa_permissions" {
  project = var.google_project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:pipeline-runner@dev-src-ftbl-home-project.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "workflow_sa_permissions" {
  project = var.google_project_id
  role    = "roles/workflows.invoker"
  member  = "serviceAccount:pipeline-runner@dev-src-ftbl-home-project.iam.gserviceaccount.com"
}
## cloud run
resource "google_cloud_run_service" "my_cloud_run_service" {
  name     = "dev-src-ftbl"
  location = "europoe-west1"  # Replace with your desired region

  template {
    spec {
      containers {
        image = "gcr.io/cloudrun/hello"
      }
      service_account_name = "pipeline-runner@dev-src-ftbl-home-project.iam.gserviceaccount.com"
    }
  }
}
## workflow
resource "google_workflows_workflow" "my_workflow" {
  name   = "src-ftbl-process"
  description     = "workflow to process src ftbl data pipeline"
  source_contents = templatefile("../../workflow/src-ftbl-processing.yaml",{})
  service_account = "pipeline-runner@dev-src-ftbl-home-project.iam.gserviceaccount.com"
}
## artifact registry to enable
