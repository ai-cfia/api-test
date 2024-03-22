from googleapi import google

def get_google_search_urls(query: str, num_results: int = 100) -> list[str]:
    links = []
    search_results = google.search(query, num_results)
    print(search_results[0].google_link )
    links.append(search_results[0].google_link )
    return links
