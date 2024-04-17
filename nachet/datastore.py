from concurrent.futures import ThreadPoolExecutor

from azure.storage.blob import BlobServiceClient, ContainerClient


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


def get_testing_image(blob_path: str,
    blob_service_client: BlobServiceClient,
    seed_name: str, key_word: str = "testing") -> list[str]:
    """
    Get the blobs of testing images from Azure Blob Storage.

    Args:
        blob_path (str): The path to the blob containers.
        blob_service_client (BlobServiceClient): The BlobServiceClient object.
        seed_name (list[str]): A list of seed names.
        key_word (str, optional): The keyword to filter the blob names. Defaults to "testing".

    Returns:
        list[str]: A dictionary containing the seed names as keys and the corresponding image blobs as values.
    """

    def get_blob_urls(container: ContainerClient) -> list[str]:
        """
        Get the blobs in a container.

        Args:
            container (ContainerClient): The ContainerClient object.

        Returns:
            list: A list of blob.
        """

        return [
            container.get_blob_client(blob.name).download_blob().readall()
            for blob in container.list_blobs()
            if seed_name in blob.name and key_word in blob.name
        ]

    container_list = blob_service_client.list_containers(name_starts_with=blob_path)
    containers = [blob_service_client.get_container_client(c.name) for c in container_list]

    with ThreadPoolExecutor() as executor:
        images = sum(executor.map(get_blob_urls, containers), [])

    return images


def get_user_image(blob_path: list[str],
    blob_service_client: BlobServiceClient,
    seed_name: list[str], key_word: str = "user") -> list[str]:
    pass

def get_image_from_folder(blob_path: str) -> list[str]:
    pass
