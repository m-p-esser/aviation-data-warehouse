# GCP Provider

provider "google" {
  credentials = file(var.gcp_deployment_sa_key)
  project = var.gcp_project_id
  region = var.gcp_default_region
}