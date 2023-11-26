""" Module for interacting with Google Cloud Storage 
using GCP Credentials Prefect Block"""

from google.cloud import storage
from prefect_gcp import GcpCredentials


def download_blob_to_file(
    bucket_name: str,
    source_blob_name: str,
    destination_file_name: str,
    gcp_credential_block_name: str,
    **kwargs: dict,
) -> storage.bucket.Bucket.blob:
    """Downloads a blob from the bucket."""

    gcp_credentials = GcpCredentials.load(gcp_credential_block_name)
    storage_client = gcp_credentials.get_cloud_storage_client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name, **kwargs)

    return blob


def download_blob_into_memory(
    bucket_name: str, blob_name: str, gcp_credential_block_name: str, **kwargs: dict
) -> str:
    """Downloads a blob into memory."""

    gcp_credentials = GcpCredentials.load(gcp_credential_block_name)
    storage_client = gcp_credentials.get_cloud_storage_client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(blob_name)
    contents = blob.download_as_string(**kwargs)

    return contents


def upload_blob_from_memory(
    bucket_name: str,
    contents,
    destination_blob_name: str,
    gcp_credential_block_name: str,
    **kwargs: dict,
) -> storage.bucket.Bucket.blob:
    """Uploads a file to the bucket."""

    gcp_credentials = GcpCredentials.load(gcp_credential_block_name)
    storage_client = gcp_credentials.get_cloud_storage_client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents, **kwargs)

    return blob


def upload_blob_from_file(
    bucket_name: str,
    source_file_name: str,
    destination_blob_name: str,
    gcp_credential_block_name: str,
    **kwargs: dict,
) -> storage.bucket.Bucket.blob:
    """Uploads a file to the bucket."""

    gcp_credentials = GcpCredentials.load(gcp_credential_block_name)
    storage_client = gcp_credentials.get_cloud_storage_client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name, **kwargs)

    return blob
