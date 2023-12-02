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

resource "google_bigquery_dataset" "dev" {
  dataset_id                 = "dev"
  description                = "Schema containing Tables of the Development Environment"
  location                   = var.gcp_default_region
  delete_contents_on_destroy = true

}

resource "google_bigquery_table" "flights-dev" {
  dataset_id  = "dev"
  table_id    = "flights"
  description = "Information about Flights sourced Flightrader24"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    source_uris   = [format("%s://%s/%s.%s", "gs", "flightradar24-flights-dev", "flights-*", "parquet")]
  }
}

resource "google_bigquery_dataset" "test" {
  dataset_id                 = "test"
  description                = "Schema containing Tables of the Test Environment"
  location                   = var.gcp_default_region
  delete_contents_on_destroy = true

}

resource "google_bigquery_table" "flights-test" {
  dataset_id  = "test"
  table_id    = "flights"
  description = "Information about Flights sourced Flightrader24"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    source_uris   = [format("%s://%s/%s.%s", "gs", "flightradar24-flights-test", "flights-*", "parquet")]
  }
}

resource "google_bigquery_dataset" "prod" {
  dataset_id                 = "prod"
  description                = "Schema containing Tables of the Production Environment"
  location                   = var.gcp_default_region
  delete_contents_on_destroy = true

}

resource "google_bigquery_table" "flights-prod" {
  dataset_id  = "prod"
  table_id    = "flights"
  description = "Information about Flights sourced Flightrader24"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    source_uris   = [format("%s://%s/%s.%s", "gs", "flightradar24-flights-prod", "flights-*", "parquet")]
  }
}
