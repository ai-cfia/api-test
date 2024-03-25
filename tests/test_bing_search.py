import unittest
from finesse.bing_search import search_bing_urls

class TestBingSearch(unittest.TestCase):
    def test_get_bing_search_urls(self):
        query = "Canada Food Inspection Agency"
        num_results = 100
        urls = search_bing_urls(query, num_results)
        self.assertEqual(len(urls), num_results)
        self.assertTrue(all(url.startswith("http") for url in urls))

if __name__ == "__main__":
    unittest.main()
