import io
from pathlib import Path

from azure.storage.blob import BlobServiceClient
from kedro.config import MissingConfigException, OmegaConfigLoader
from kedro.framework.project import settings

conf_path = str(
    Path("/Users/gziz/Desktop/mlops/reto/tca-pipelines") / settings.CONF_SOURCE
)
conf_loader = OmegaConfigLoader(conf_source=conf_path)

try:
    credentials = conf_loader["credentials"]
except MissingConfigException:
    credentials = {}


def upload_to_blob_storage(data, container_name, blob_name, account_name, account_key):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key,
    )
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {blob_name} to container {container_name}.")


def upload_reports_node(
    cancellation_percentages,
    median_values,
    mean_values,
    agencia_distribution,
    canal_distribution,
):
    account_name = credentials["azure_blob"]["account_name"]
    account_key = credentials["azure_blob"]["account_key"]
    container_name = credentials["azure_blob"]["container_name"]

    report_files = {
        "cancellation_percentages.csv": cancellation_percentages,
        "median_values.csv": median_values,
        "mean_values.csv": mean_values,
        "agencia_distribution.csv": agencia_distribution,
        "canal_distribution.csv": canal_distribution,
    }

    for file_name, df in report_files.items():
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        upload_to_blob_storage(
            buffer.getvalue(), container_name, file_name, account_name, account_key
        )
