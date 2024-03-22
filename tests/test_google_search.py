import unittest
from finesse.google_search import get_google_search_urls

class TestGoogleSearch(unittest.TestCase):
    def test_get_google_search_urls(self):
        query = "Canada Food Inspection Agency"
        num_results = 10
        urls = get_google_search_urls(query, num_results)
        self.assertEqual(len(urls), num_results)
        self.assertTrue(all(url.startswith("http") for url in urls))

if __name__ == "__main__":
    unittest.main()