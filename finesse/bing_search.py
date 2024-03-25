
import os
from pprint import pprint
import requests
from dotenv import load_dotenv
import os

def search_bing_urls(query: str, num_results: int = 100) -> list[str]:
    load_dotenv()
    urls = []
    endpoint = os.getenv("BING_ENDPOINT") + "/v7.0/search"
    subscription_key = os.getenv("BING_SEARCH_KEY")
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt, 'count': 50 }
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        print("\nHeaders:\n")
        print(response.headers)

        print("\nJSON Response:\n")
        pprint(response.json())

    except Exception as ex:
        raise ex
