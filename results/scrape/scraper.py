from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter, Retry


def retrieve_url(url: str) -> str:
    """Retrieve the content of a URL as string.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The content of the URL
    """
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))

    headers = {"User-Agent": "Mozilla/5.0"}

    response = session.get(url, headers=headers, timeout=60)
    return response.text


def make_soup(url: str) -> BeautifulSoup:
    """Create a BeautifulSoup object from a URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        BeautifulSoup: The BeautifulSoup object.
    """
    html = retrieve_url(url)
    return BeautifulSoup(html, "html.parser")


soup = make_soup(
    "https://www.englandrugby.com/fixtures-and-results/search-results?competition=1699&division=56619&season=2024-2025#results"
)
print(soup.find("div", class_="resultWrapper"))
