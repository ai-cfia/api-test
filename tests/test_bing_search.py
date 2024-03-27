import unittest
from finesse.bing_search import BingSearch
from dotenv import load_dotenv
import os
class TestBingSearch(unittest.TestCase):
    def test_search_urls(self):
        load_dotenv()
        endpoint = os.getenv("BING_ENDPOINT")
        subscription_key = os.getenv("BING_SEARCH_KEY")
        bing_search = BingSearch(endpoint, subscription_key)

        query = "Canada Food Inspection Agency"
        num_results = 100

        urls, elapsed_time = bing_search.search_urls(query, num_results)

        self.assertEqual(len(urls), num_results)
        self.assertTrue(all(url.startswith("http") for url in urls))
        self.assertIsInstance(elapsed_time, float)

if __name__ == "__main__":
    unittest.main()
