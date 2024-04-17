import openpyxl
import base64
import requests
import json


def start_testing(amount: int, data: list, backend_url: str, models: list[str]) -> dict:
    """
    Start the testing process.

    Args:
        amount (int): The number of tests to perform.
        data (list): A list containing the seeds name and testing folders.
        backend_url (str): The URL of the backend.
        bsc: The BSC object.

    Returns:
        dict: A dictionary containing the results of the testing process.
    """

    images_to_test = [ base64.b64encode(blob).decode("utf8") for blob in data[:amount]]

    for img in images_to_test:
        for model in models:
            paylaoad = {
                "model_name":model,
                "validator": "nachet_testing_image",
                "folder_name": "api_test_nachet",
                "container_name": "testing-images",
                "imageDims": [100, 100],
                "image": img
            }

            headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },

            response = requests.post(backend_url + "/inf", json=paylaoad, headers=headers)
            result = response.json()

            print()

def test_inference(image: str, backend_url: str) -> dict:
    pass
