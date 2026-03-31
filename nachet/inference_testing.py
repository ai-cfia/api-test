import base64
import requests
import time


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

    results = {model: {} for model in models}

    images_to_test = [base64.b64encode(blob).decode("utf8") for blob in data[:amount]]

    i = 1
    for img in images_to_test:

        key = f"image{i:02d}"
        i += 1
        for model in models:
            payload = {
                "model_name": model,
                "validator": "nachet_testing_image",
                "folder_name": "api_test_nachet",
                "container_name": "testing-images",
                "imageDims": [100, 100],
                "image": "data:image/PNG;base64," + img
            }

            headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }

            start = time.perf_counter()
            response = requests.post(
                backend_url + "/inf", json=payload, headers=headers).json()
            end = time.perf_counter() - start

            boxes = response[0]["boxes"]

            print(key)
            print(f"number of seed detecte: {len(boxes)}")

            topN = []

            if boxes[0].get("topN"):
                for box in boxes:
                    topN.extend([score.get("label") for score in box.get("topN")])

            results.get(model).update({
                key: {
                    "labels": [box.get("label") for box in boxes],
                    "topN": topN,
                    "nb_seeds": response[0].get("totalBoxes"),
                    "request_time": end,
                }
            })

    return results

def test_inference(image: str, backend_url: str) -> dict:
    pass
