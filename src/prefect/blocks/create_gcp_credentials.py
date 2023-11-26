"""Programmatically create GCP Credential Block for Prefect"""

from prefect_gcp import GcpCredentials

from src.utils import load_env_vars

env_vars = load_env_vars()

PREFECT_BLOCK_NAME_GCP_CREDENTIALS_BLOCK_NAME = (
    f"{env_vars['GCP_PROJECT_ID']}-{env_vars['GCP_DEPLOYMENT_SERVICE_ACCOUNT']}"
)

with open(f".secrets/deployment_sa_account.json", "r") as f:
    service_account = f.read()

gcp_credentials_block = GcpCredentials(service_account_info=service_account).save(
    name=PREFECT_BLOCK_NAME_GCP_CREDENTIALS_BLOCK_NAME, overwrite=True
)
