import re
import requests
from bs4 import BeautifulSoup
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


def _not_second_opinion(elem_txt):
    return str(elem_txt).lower() != "second opinion"


def get_review_links(list_url):
    response = requests.get(list_url)
    response.raise_for_status()

    list_page_soup = BeautifulSoup(response.text, "html.parser")
    list_soup = list_page_soup.find(class_="content")
    rev_link_elems = list_soup.findAll(href=re.compile("viewreview.php"),
                                       string=_not_second_opinion)
    review_links = [rev_link.get('href') for rev_link in rev_link_elems]
    return review_links


def get_anime_title(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        title = review_page_soup.find('h1').text
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing a title.")
    return title