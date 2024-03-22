from googlesearch import search

def get_google_search_urls(query: str, num_results: int = 100) -> list[str]:
    """
    Retrieves a list of Google search result URLs for the given query.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of search results to retrieve. Defaults to 100.

    Returns:
        list[str]: A list of URLs representing the search results.
    """
    num_results -= 2 # 2 extra urls are added by googlesearch library
    links = []
    for url in search(query, num_results, sleep_interval=1):
        links.append(url)
    return links
