"""Programmatically create Flightsapi API Key for Prefect"""

from prefect.blocks.system import Secret
from src.utils import load_env_vars

env_vars = load_env_vars()

GCP_PROJECT_ID = env_vars["GCP_PROJECT_ID"]

FLIGHTRADAR24_USERNAME = env_vars["FLIGHTRADAR24_USERNAME"]
FLIGHTRADAR24_USERNAME_BLOCK_NAME = f"{GCP_PROJECT_ID}-flightradar24-username"

flightsrader24_username_block = Secret(value=FLIGHTRADAR24_USERNAME).save(
    name=FLIGHTRADAR24_USERNAME_BLOCK_NAME, overwrite=True
)

FLIGHTRADAR24_PASSWORD = env_vars["FLIGHTRADAR24_PASSWORD"]
FLIGHTRADAR24_PASSWORD_BLOCK_NAME = f"{GCP_PROJECT_ID}-flightradar24-password"

flightsrader24_password_block = Secret(value=FLIGHTRADAR24_PASSWORD).save(
    name=FLIGHTRADAR24_PASSWORD_BLOCK_NAME, overwrite=True
)
