from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError

class DatastoreErrors(Exception):
    pass

def get_blob_client(connection: str) -> BlobServiceClient:
    """
    Returns a BlobServiceClient object initialized with the provided connection
    string.

    Args:
        connection (str): The connection string for the Azure Blob Storage
        account.

    Returns:
        BlobServiceClient: The initialized BlobServiceClient object.

    Raises:
        DatastoreErrors: If the blob client cannot be retrieved.
    """
    try:
        return BlobServiceClient.from_connection_string(connection)
    except ValueError as error:
        raise DatastoreErrors("could not retrieve the blob client") from error


def get_testing_image(amount: int, blob_path: str,
                      blob_service_client: BlobServiceClient) -> list[str]:
    pass


def get_user_image(amount: int, blob_path: str | list,
                   blob_service_client: BlobServiceClient) -> list[str]:
    pass
