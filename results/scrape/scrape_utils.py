import requests
from bs4 import BeautifulSoup
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


def extract_event(event_class: str) -> str:
    """Extract the type of event from the event string.

    Args:
        event_class (str): The class name containing the event type

    Returns:
        str: The type of event.
    """
    events: dict[str, str] = {
        "try": "Try",
        "conversion": "Conversion",
        "penalty": "Penalty",
        "drop-goal": "Drop Goal",
        "yellow-card": "Yellow Card",
        "red-card": "Red Card",
        "penalty-try": "Penalty Try",
    }

    for key, value in events.items():
        if key in event_class:
            return value

    err = f"Event type not found: {event_class}"
    raise ValueError(err)
