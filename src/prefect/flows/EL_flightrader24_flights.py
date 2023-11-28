""" Extract Flights from Flightrader24 API and load them into a GCS Bucket """

import datetime
import uuid

import pandas as pd
from FlightRadar24 import FlightRadar24API
from prefect.artifacts import create_table_artifact
from prefect.logging import get_run_logger
from prefect import flow, task
from prefect.blocks.system import Secret
from src.gcs import upload_blob_from_memory
from src.schema.raw import FlightsSchema
from src.utils import load_env_vars


@task(log_prints=True)
def construct_api_client() -> FlightRadar24API:
    """Create FlightRadar24 API Client"""
    env_vars = load_env_vars()
    GCP_PROJECT_ID = env_vars["GCP_PROJECT_ID"]

    username = Secret.load(f"{GCP_PROJECT_ID}-flightradar24-username")
    password = Secret.load(f"{GCP_PROJECT_ID}-flightradar24-password")

    api_client = FlightRadar24API(user=username.get(), password=password.get())

    return api_client


@task
def get_flights(api_client: FlightRadar24API) -> list[dict]:
    """Request Flights from Flightradar"""

    logger = get_run_logger()
    flights = api_client.get_flights()
    flights = [f.__dict__ for f in flights]
    logger.info(f"Response from Flightradar contains {len(flights)} flights")

    return flights


@task
def store_flights_in_df(flights: list[dict]) -> pd.DataFrame:
    """Store Flights in Dataframe"""

    logger = get_run_logger()
    flights_df = pd.DataFrame(flights)
    create_table_artifact(key=str(uuid.uuid4()), table=flights)
    logger.info(
        f"Dataframe contains: {flights_df.shape[0]} rows and {flights_df.shape[1]} columns"
    )
    logger.info(flights_df.dtypes)

    logger.info(flights_df.head(10))

    return flights_df


@task
def validate_flights(flights_df: pd.DataFrame):
    """Validate Data of Flights Dataframe"""
    logger = get_run_logger()
    validation = FlightsSchema.validate(flights_df)
    logger.info("Flights Data has been validated sucessfully")
    return validation


@task
def load_df_to_gcs_bucket(flights_df: pd.DataFrame):
    """Store Flights in GCS Bucket"""

    logger = get_run_logger()

    flights_df["requested_at"] = pd.to_datetime(datetime.datetime.now())
    contents = flights_df.to_parquet(engine="pyarrow")
    rounded_datetime_str = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

    env_vars = load_env_vars()

    blob = upload_blob_from_memory(
        bucket_name=f"flightrader24-flights-{env_vars['ENV']}",
        contents=contents,
        destination_blob_name=f"flights-{rounded_datetime_str}.parquet",
        gcp_credential_block_name=f"{env_vars['GCP_PROJECT_ID']}-{env_vars['GCP_DEPLOYMENT_SERVICE_ACCOUNT']}",
    )
    logger.info(f"Created Blob '{blob}'")


@flow()
def extract_load_flightradar24_flights():
    """Extract Flights from Flightrader24 API and load them into a GCS Bucket"""
    api_client = construct_api_client()
    flights = get_flights(api_client)
    flights_df = store_flights_in_df(flights)
    validation = validate_flights(flights_df)
    load_df_to_gcs_bucket(flights_df, wait_for=[validation])


if __name__ == "__main__":
    extract_load_flightradar24_flights()
