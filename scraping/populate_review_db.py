import re
import string
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
    rev_link_elems = list_soup.find_all(href=re.compile("viewreview.php"),
                                        string=_not_second_opinion)
    review_links = [rev_link.get('href') for rev_link in rev_link_elems]
    return review_links


def get_title(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        title = review_page_soup.find('h1').text
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing a title.")
    return title


def get_aka(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        aka_tag = review_page_soup.find('b', text=re.compile("AKA"))
        aka = aka_tag.next_sibling.strip()
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing alternative names.")
    return aka


def get_genre(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        genre_tag = review_page_soup.find('b', text=re.compile("Genre"))
        genre = genre_tag.next_sibling.strip()
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing its genre.")
    return genre


def get_content_rating(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        content_rating_tag = review_page_soup.find('b', text=re.compile("Content Rating"))
        content_rating = content_rating_tag.next_sibling
        if "(" in content_rating:
            explanation_start = content_rating.find("(")
            content_rating = content_rating[:explanation_start]
        content_rating = content_rating.strip()
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing its content rating.")
    return content_rating


def get_length_info(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        length_tag = review_page_soup.find('b', text=re.compile("Length"))
        length_details = length_tag.next_sibling.split(",")
        media_type = length_details[0].strip()
        num_episodes = 1 if len(length_details) < 3 else int(length_details[1].split()[0])
        mins_per_episode = int(length_details[-1].split()[0])
        length_info = (media_type, num_episodes, mins_per_episode)
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing its length information.")
    return length_info


def get_distributor(review_url):
    response = requests.get(review_url)
    response.raise_for_status()

    review_page_soup = BeautifulSoup(response.text, "html.parser")
    try:
        distributor_tag = review_page_soup.find('b', text=re.compile("Distributor"))
        distributor_link = distributor_tag.find_next_sibling('a')
        if distributor_link:
            distributor = distributor_link.string
        else:
            distributor_details = distributor_tag.next_sibling
            by_location = distributor_details.find("by")
            distributor_start = by_location + len("by ")
            DELIMETERS = "[{}]".format(string.punctuation)
            distributor = re.split(DELIMETERS, distributor_details[distributor_start:])[0]
    except AttributeError:
        raise MissingAnimeDetailError("This anime's review is missing its distributor.")
    return distributor
