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
def get_flights(api_client: FlightRadar24API) -> tuple[list[dict], datetime.datetime]:
    """Request Flights from Flightradar24"""

    logger = get_run_logger()
    flights = api_client.get_flights(details=False)
    flights = [f.__dict__ for f in flights]
    requested_at = datetime.datetime.now()
    logger.info(f"Requested Flights24 at {requested_at.strftime("%Y-%m-%d-%H:%M:%S")}")
    logger.info(f"Response from Flightradar24 contains {len(flights)} flights")

    return (flights, requested_at)


@task
def store_flights_in_df(flights: list[dict], requested_at: datetime.datetime) -> pd.DataFrame:
    """Store Flights in Dataframe"""

    logger = get_run_logger()
    flights_df = pd.DataFrame(flights)
    flights_df["requested_at"] = pd.to_datetime(requested_at)
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
def load_df_to_gcs_bucket(flights_df: pd.DataFrame, requested_at: datetime.datetime):
    """Store Flights in GCS Bucket"""

    logger = get_run_logger()

    contents = flights_df.to_parquet(engine="pyarrow")
    rounded_datetime_str = requested_at.strftime("%Y-%m-%d-%H:%M:%S")

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
    flights, requested_at = get_flights(api_client)
    flights_df = store_flights_in_df(flights, requested_at)
    validation = validate_flights(flights_df)
    load_df_to_gcs_bucket(flights_df, requested_at, wait_for=[validation])


if __name__ == "__main__":
    extract_load_flightradar24_flights()
