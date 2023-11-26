"""Programmatically create Flightsapi API Key for Prefect"""

from prefect.blocks.system import Secret
from src.utils import load_env_vars

env_vars = load_env_vars()

FLIGHTSAPI_API_KEY = env_vars["FLIGHTSAPI_API_KEY"]
GCP_PROJECT_ID = env_vars["GCP_PROJECT_ID"]
FLIGHTSAPI_API_KEY_BLOCK_NAME = f"{GCP_PROJECT_ID}-flightsapi-api-key"

flightapi_api_key_block = Secret(value=FLIGHTSAPI_API_KEY).save(
    name=FLIGHTSAPI_API_KEY_BLOCK_NAME, overwrite=True
)
