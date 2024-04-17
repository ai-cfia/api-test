import os
import time
import re

from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError


load_dotenv()

# Environment variable
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
SEEDS_NAME = os.getenv("SEEDS_NAME")
TESTING_FOLDERS = os.getenv("TESTING_FOLDERS")


class DatastoreErrors(Exception):
    pass

def format_list_env():
    """
    Format the list of environment variable for the seeds name and testing
    folders.
    """
    seeds_name = [name.strip() for name in SEEDS_NAME.split(',')]
    testing_folders = [name.strip() for name in TESTING_FOLDERS.split(',')]
    return seeds_name, testing_folders


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
    blob_service_client: BlobServiceClient,
    seed_name: list[str], key_word: str = "testing") -> list[str]:
    """
    2024-taran-verified-seedid
    """

    def get_blob_urls(container: ContainerClient) -> list[str]:
        """
        """
        return [
            container.get_blob_client(name).url
            for name in container.list_blob_names()
            if key_word in name
        ]

    container_list = blob_service_client.list_containers(name_starts_with=blob_path)
    containers = [blob_service_client.get_container_client(c.name) for c in container_list]

    with ThreadPoolExecutor() as executor:
        img_url = sum(executor.map(get_blob_urls, containers), [])

    seed_testing = {
        seed: [url for url in img_url if seed.split(" ")[1] in url]
        for seed in seed_name
    }

    # Divide the amount per seed to select a number of image to test the models with
    nb_image_per_seed = round(amount / len(seed_name))

    print(seed_testing[seed_name[0]])

    print(seed_name[0])

    return seed_testing


def get_user_image(amount: int, blob_path: list[str],
                   blob_service_client: BlobServiceClient) -> list[str]:
    pass

if __name__ == "__main__":
    seconds = time.perf_counter()
    seeds_name, testing_folders = format_list_env()
    bsc = get_blob_client(AZURE_STORAGE_CONNECTION_STRING)
    get_testing_image(55, testing_folders[1], bsc, seeds_name)
    print(f"Took: {'{:10.4f}'.format(time.perf_counter() - seconds)} seconds")
