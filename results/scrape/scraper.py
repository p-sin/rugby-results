from dataclasses import dataclass
from typing import Any

from results.scrape import scrape_utils as utils


@dataclass
class Scraper:
    config: dict[Any, Any]

    def scrape(self) -> None:
        utils.make_soup(self.config["url"])


soup = utils.make_soup(
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
    print(f"Date of match: {date_div.text}")

    results = wrapper.find_all("div", recursive=False)[1:]

    for result in results:
        fixture_data = result.find("div")
        print(f"Home team: {fixture_data.find("div").find("a").text}")
        print(
            f"Away team: {fixture_data.find_all("div", recursive=False)[2].find("a").text}"
        )

        scores = [
            score.text
            for score in fixture_data.find_all("div", recursive=False)[1].find_all(
                "span"
            )
        ]
        print(f"Scores: {scores}")

        match_info_url = (
            result.find("div", class_="coh-style-clicktoinfo").find("a").get("href")
        )

        match_info = utils.make_soup(
            url=f"https://www.englandrugby.com/{match_info_url}"
        )
        all_events = match_info.find_all(
            "div", class_="c042-key-match-events-accordion-body-info"
        )

        home_events = all_events[0].find_all(
            "div", class_="c042-key-match-events-items"
        )
        for event_num, event in enumerate(home_events):
            try:
                event_class = event.find("div").get("class")
                print(
                    f"Home event ({event_num}): {utils.extract_event(event_class[1])}"
                )
            except AttributeError:
                continue

        away_events = all_events[2].find_all(
            "div", class_="c042-key-match-events-items"
        )
        for event_num, event in enumerate(away_events):
            try:
                event_class = event.find("div").get("class")
                print(
                    f"Away event ({event_num}): {utils.extract_event(event_class[1])}"
                )
            except AttributeError:
                continue


# bs4.element.Tag
