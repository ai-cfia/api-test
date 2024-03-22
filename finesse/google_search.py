from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def search_google_urls(query: str, num_results: int = 100) -> list[str]:
    """
    Retrieves a list of Google search result URLs for the given query using the Google API.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of search results to retrieve. Defaults to 100.

    Returns:
        list[str]: A list of URLs representing the search results.

    Raises:
        Exception: If the request limit is exceeded (error 429 Too Many Requests).
    """
    load_dotenv()
    links = []
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    results = google_search(query, api_key, cse_id, start=11)
    for item in results:
        links.append(item['link'])
    return links
