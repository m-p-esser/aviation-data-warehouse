"""Programmatically store selected, insensitive Env Variables and store them in String Blocks"""

from prefect.blocks.system import String
from src.utils import load_env_vars

env_vars = load_env_vars()

env_var_keys = [
    "GCP_PROJECT_ID",
    "GCP_DEFAULT_REGION",
    "GCP_DEFAULT_ZONE",
    "GCP_DEPLOYMENT_SERVICE_ACCOUNT",
    "PREFECT_VERSION",
    "PYTHON_VERSION",
    "ENV"
]

GCP_PROJECT_ID = env_vars["GCP_PROJECT_ID"]

for k in env_var_keys:

    key = k.lower().replace("_","-")
    value = env_vars[k]
    block_name = f"{GCP_PROJECT_ID}-{key}"

    block = String(value=value).save(
        name=block_name, overwrite=True
    )
