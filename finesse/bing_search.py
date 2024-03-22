import requests
import random

def get_bing_search_urls(query: str, num_results: int = 100) -> list[str]:
    urls = []
    headers = {'User-Agent': get_useragent()}
    cookies = get_cookies()
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    res = requests.get(url, headers=headers, cookies=cookies)
    if res.status_code == 200:
        urls.append(res.url)
    else:
        raise requests.exceptions.HTTPError(res.status_code, res.url)
    return urls

def get_cookies():
    """
    Generates cookies to avoid getting blocked during search.
    Returns:
        dict: A dictionary containing the cookies.

    Raises:
        requests.exceptions.HTTPError: If the response status code is not 200.
    """
    trend_url = 'https://youtube.com'
    response = requests.get(trend_url)
    if response.status_code == 200:
        return response.cookies.get_dict()
    else:
        raise requests.exceptions.HTTPError(f'Cookies raised {response.status_code}')



def get_useragent():
    USERAGENT_LIST = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]
    return random.choice(USERAGENT_LIST)
