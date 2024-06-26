import time
import statistics

from azure.cognitiveservices.search.websearch import WebSearchClient
from msrest.authentication import CognitiveServicesCredentials
from joblib import Memory

class BingSearch():
    """
    A class for performing web searches using the Bing Search API.
    """

    def __init__(self, endpoint, subscription_key, cache_dir):
        self.endpoint = endpoint
        self.subscription_key = subscription_key
        self.client = WebSearchClient(endpoint=self.endpoint, credentials=CognitiveServicesCredentials(self.subscription_key))
        self.client.config.base_url = '{Endpoint}/v7.0' # Temporary change to fix the error. Issue opened https://github.com/Azure/azure-sdk-for-python/issues/34917
        self.cache_dir = cache_dir
        self.memory = Memory(cache_dir, verbose=0)
        self.search_urls = self.memory.cache(self.search_urls, ignore=['self'])

    def search_urls(self, query: str, num_results: int = 100) -> tuple[list[str], float]:
        """
        Search for URLs using the Bing Search API.

        Args:
            query (str): The search query.
            num_results (int, optional): The number of results to retrieve. Defaults to 100.

        Returns:
            tuple[list[str], float]: A tuple containing a list of URLs and the average elapsed time for the search.
        """
        urls = []
        elapsed_time = []
        offset = 0
        # Limit of 50 results per query and Bing Search return less than 50 web results
        while len(urls) < num_results:
            start_time = time.time()
            web_data = self.client.web.search(query=query, market="en-ca", count=50, response_filter=["Webpages"], offset=offset)
            elapsed_time.append(time.time() - start_time)
            if hasattr(web_data, 'web_pages') and web_data.web_pages is not None:
                urls.extend([item.url for item in web_data.web_pages.value])
            try:
                offset += len([item.url for item in web_data.web_pages.value])
            except AttributeError:
                break
        urls = urls[:num_results]
        return urls, statistics.mean(elapsed_time) * 1000
