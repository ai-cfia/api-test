
import os
import requests

from dotenv import load_dotenv

from datastore import get_blob_client
from nachet_ui import actions

load_dotenv()

# Environment variable
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
SEEDS_NAME = os.getenv("SEEDS_NAME")
TESTING_FOLDERS = os.getenv("TESTING_FOLDERS")
NACHET_BACKEND_URL = os.getenv("NACHET_BACKEND_URL")


def format_list_env():
    """
    Format the list of environment variable for the seeds name and testing
    folders.
    """
    seeds_name = [name.strip() for name in SEEDS_NAME.split(',')]
    testing_folders = [name.strip() for name in TESTING_FOLDERS.split(',')]
    return seeds_name, testing_folders


def app_initialisation():
    url = NACHET_BACKEND_URL + "/model-endpoints-metadata"
    response = requests.get(url)
    seeds_name, testing_folders = format_list_env()
    bsc = get_blob_client(AZURE_STORAGE_CONNECTION_STRING)
    return seeds_name, testing_folders, bsc, NACHET_BACKEND_URL


def main():
    actions[5](*app_initialisation())

if __name__ == "__main__":
   main()
