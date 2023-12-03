""" Extract Aiports from Flightrader24 API and load them into a GCS Bucket """

import datetime
import uuid

import pandas as pd
from FlightRadar24 import FlightRadar24API
from prefect.artifacts import create_table_artifact
from prefect.logging import get_run_logger
from prefect import flow, task
from prefect.blocks.system import Secret
from src.gcs import upload_blob_from_memory
from src.schema.raw import AirportsSchema
from src.utils import load_env_vars


@task
def construct_api_client() -> FlightRadar24API:
    """Create FlightRadar24 API Client"""
    env_vars = load_env_vars()
    GCP_PROJECT_ID = env_vars["GCP_PROJECT_ID"]

    username = Secret.load(f"{GCP_PROJECT_ID}-flightradar24-username")
    password = Secret.load(f"{GCP_PROJECT_ID}-flightradar24-password")

    api_client = FlightRadar24API(user=username.get(), password=password.get())

    return api_client


@task
def get_airports(api_client: FlightRadar24API) -> tuple[list[dict], datetime.datetime]:
    """Request Airports from Flightradar24"""

    logger = get_run_logger()
    airports = api_client.get_airports()
    airports = [a.__dict__ for a in airports]
    requested_at = datetime.datetime.now()
    logger.info(f"Requested Flights24 at {requested_at.strftime('%Y-%m-%d-%H:%M:%S')}")
    logger.info(f"Response from Flightradar24 contains {len(airports)} airports")

    return (airports, requested_at)


@task
def store_airports_in_df(
    airports: list[dict], requested_at: datetime.datetime
) -> pd.DataFrame:
    """Store Airports in Dataframe"""

    logger = get_run_logger()

    airports_df = pd.DataFrame(airports)
    airports_df["requested_at"] = pd.to_datetime(requested_at)
    airports_df = airports_df.astype({"altitude": int})
    airports_df.drop(columns=["_Airport__raw_information"], inplace=True)

    create_table_artifact(key=str(uuid.uuid4()), table=airports)
    logger.info(
        f"Dataframe contains: {airports_df.shape[0]} rows and {airports_df.shape[1]} columns"
    )
    logger.info(airports_df.dtypes)

    logger.info(airports_df.head(10))

    return airports_df


@task
def validate_airports(airports_df: pd.DataFrame):
    """Validate Data of Airports Dataframe"""
    logger = get_run_logger()
    validation = AirportsSchema.validate(airports_df)
    logger.info("Flights Data has been validated sucessfully")
    return validation


@task
def load_df_to_gcs_bucket(airports_df: pd.DataFrame, requested_at: datetime.datetime):
    """Store Aiports in GCS Bucket"""

    logger = get_run_logger()

    contents = airports_df.to_parquet(engine="pyarrow")
    rounded_datetime_str = requested_at.strftime("%Y-%m-%d-%H:%M:%S")

    env_vars = load_env_vars()

    blob = upload_blob_from_memory(
        bucket_name=f"flightradar24-airports-{env_vars['ENV']}",
        contents=contents,
        destination_blob_name=f"airports-{rounded_datetime_str}.parquet",
        gcp_credential_block_name=f"{env_vars['GCP_PROJECT_ID']}-{env_vars['GCP_DEPLOYMENT_SERVICE_ACCOUNT']}",
    )
    logger.info(f"Created Blob '{blob}'")


@flow(retries=3, retry_delay_seconds=5)
def extract_load_flightradar24_airports():
    """Extract Flights from Flightrader24 API and load them into a GCS Bucket"""
    api_client = construct_api_client()
    airports, requested_at = get_airports(api_client)
    airports_df = store_airports_in_df(airports, requested_at)
    validation = validate_airports(airports_df)
    load_df_to_gcs_bucket(airports_df, requested_at, wait_for=[validation])


if __name__ == "__main__":
    extract_load_flightradar24_airports()
