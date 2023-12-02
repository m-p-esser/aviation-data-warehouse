resource "google_storage_bucket" "flights-dev" {
  name     = format("%s-%s", "flightradar24-flights", "dev")
  location = var.gcp_default_region
}

resource "google_storage_bucket" "flights-test" {
  name     = format("%s-%s", "flightradar24-flights", "test")
  location = var.gcp_default_region
}

resource "google_storage_bucket" "flights-prod" {
  name     = format("%s-%s", "flightradar24-flights", "prod")
  location = var.gcp_default_region
}