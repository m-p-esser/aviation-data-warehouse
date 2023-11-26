resource "google_storage_bucket" "flights" {
  name = format("%s-%s","flightrader24-flights",var.env)
  location = var.gcp_default_region
}