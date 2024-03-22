from googlesearch import search

def get_google_search_urls(query: str, num_results: int = 100) -> list[str]:
    links = []
    for url in search(query, num_results, sleep_interval=1):
        links.append(url)
    return links
