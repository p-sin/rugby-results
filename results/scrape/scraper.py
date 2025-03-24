from typing import Any

import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter, Retry

config: dict[str, Any] = {
    "Comp1": "https://www.englandrugby.com/fixtures-and-results/search-results?competition=173&division=57597&season=2024-2025#results"
}


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


def extract_result_wrappers(soup: BeautifulSoup) -> list[Tag]:
    """Extract the result wrappers from the BeautifulSoup object.

    A result wrapper contains all the results for a specific week.
    This is found in the 'cardContainer' div, which is the lowest level parent containing
    the results data.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.

    Returns:
        list[Tag]: A list of all the result wrappers.
    """
    all_results = soup.find("div", id="results")

    if not all_results:
        err = "No results found on page"
        raise ValueError(err)

    # Drill down to the 'cardContainer' which has all the results in it
    card_container = (
        all_results.find("div")  # type: ignore
        .find("div", id="fnrcardData")
        .find("div", id="cardContainer")
    )

    # Result wrappers contain all results for a week
    result_wrappers: list[Tag] = card_container.find_all(
        "div", class_="resultWrapper", recursive=False
    )

    return result_wrappers


def identify_event(event_class: str) -> str:
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


def extract_events(event_data: BeautifulSoup, team_key: int) -> list[str]:
    """Extract all game events for a team from the complete match event data.

    Args:
        event_data (BeautifulSoup): The BeautifulSoup object containing the event data.
        team_key (int): Either 0 or 2, the index of either the home or away team in the event data.

    Returns:
        list[str]: A list of all the events for a team.
    """
    event_return: list[str] = []

    all_events = event_data.find_all(
        "div", class_="c042-key-match-events-accordion-body-info"
    )

    events = all_events[team_key].find_all("div", class_="c042-key-match-events-items")  # type: ignore
    for event in events:
        try:
            event_class = event.find("div").get("class")[1]  # type: ignore
            event_return.append(identify_event(event_class))
        except AttributeError:
            continue  # Due to page formatting, some are empty

    return event_return


def extract_match_data(result: Tag) -> tuple[str, str, list[str], list[str], list[str]]:
    """Collates all the required data for a single match.

    Args:
        result (Tag): The result tag containing all the match data.

    Returns:
        str: home team name
        str: away team name
        list[str]: scores
        list[str]: home team events
        list[str]: away team events
    """
    fixture_data = result.find("div")

    if not fixture_data:
        err = "No fixture data found"
        raise ValueError(err)

    home_team = fixture_data.find("div").find("a").text  # type: ignore
    away_team = fixture_data.find_all("div", recursive=False)[2].find("a").text  # type: ignore

    scores = [
        score.text
        for score in fixture_data.find_all("div", recursive=False)[1].find_all("span")  # type: ignore
    ]

    events_url = (
        result.find("div", class_="coh-style-clicktoinfo").find("a").get("href")  # type: ignore
    )

    event_data = make_soup(url=f"https://www.englandrugby.com/{events_url}")
    home_events = extract_events(event_data, 0)
    away_events = extract_events(event_data, 2)

    return (home_team, away_team, scores, home_events, away_events)


def process_matches(result_wrappers: list[Tag]) -> None:
    """Extract the match data from each result wrapper.

    Args:
        result_wrappers (list[Tag]): A list of all the result wrappers.
    """
    for wrapper in result_wrappers:
        # The first div contains the date component
        date = wrapper.find("div").find("div").text

        results = wrapper.find_all("div", recursive=False)[1:]

        for result in results:
            home_team, away_team, scores, home_events, away_events = extract_match_data(
                result
            )

            print(f"Date of match: {date}")
            print(home_team)
            print(away_team)
            print(scores)
            print(home_events)
            print(away_events)


def scrape() -> None:
    for competition, url in config.items():
        print(competition)
        soup = make_soup(url)
        result_wrappers = extract_result_wrappers(soup)
        process_matches(result_wrappers)


if __name__ == "__main__":
    scrape()
