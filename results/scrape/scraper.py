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


soup = make_soup(
    "https://www.englandrugby.com/fixtures-and-results/search-results?competition=173&division=57597&season=2024-2025#results"
)

all_results = soup.find("div", id="results")

# Drill down to the 'cardContainer' which has all the results in it
card_container = (
    all_results.find("div")
    .find("div", id="fnrcardData")
    .find("div", id="cardContainer")
)

# Result wrappers contain all results for a week
result_wrappers = card_container.find_all(
    "div", class_="resultWrapper", recursive=False
)
for wrapper in result_wrappers:
    # The first div contains the date component
    date_div = wrapper.find("div").find("div")
    print(date_div.text)

    results = wrapper.find_all("div", recursive=False)[1:]

    for result in results:
        fixture_data = result.find("div")
        print(fixture_data.find("div").find("a").text)
        print(fixture_data.find_all("div", recursive=False)[2].find("a").text)

        scores = [
            score.text
            for score in fixture_data.find_all("div", recursive=False)[1].find_all(
                "span"
            )
        ]
        print(scores)

        match_info_url = (
            result.find("div", class_="coh-style-clicktoinfo").find("a").get("href")
        )

        match_info = make_soup(url=f"https://www.englandrugby.com/{match_info_url}")
        all_events = match_info.find_all(
            "div", class_="c042-key-match-events-accordion-body-info"
        )

        home_events = all_events[0].find_all(
            "div", class_="c042-key-match-events-items"
        )
        for event in home_events:
            try:
                event_class = event.find("div").get("class")
                print(extract_event(event_class[1]))
            except AttributeError:
                continue

        away_events = all_events[2].find_all(
            "div", class_="c042-key-match-events-items"
        )
        for event in away_events:
            try:
                event_class = event.find("div").get("class")
                print(extract_event(event_class[1]))
            except AttributeError:
                continue


# bs4.element.Tag
