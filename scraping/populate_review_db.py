import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from scraping.Anime import Anime
from db.connect_to_db import connect_to_db


logger = logging.getLogger(__name__)


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


def populate_review_db():
    LIST_URL = "https://www.themanime.org/reviewlist.php"
    BASE_URL = "https://www.themanime.org/"
    review_links = get_review_links(LIST_URL)

    cnx = connect_to_db()
    cursor = cnx.cursor()

    for rev_url in review_links:
        response = requests.get(BASE_URL + rev_url)
        response.raise_for_status()
        rev_soup = BeautifulSoup(response.text, "html.parser")
        anime = Anime(rev_url, rev_soup)
        anime_details = anime.to_dict()

        # TODO: Add to DB, LOGGING! AND TESTS!
        cursor.execute("INSERT INTO anime "
                       "(id, title, aka, genre, mediaType, "
                       "numEpisodes, minsPerEpisode, distributor, contentRating, revURL) VALUES "
                       "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (anime_details['id'], anime_details['title'], anime_details['aka'], anime_details['genre'],
                        anime_details['mediaType'], anime_details['numEpisodes'], anime_details['minsPerEpisode'],
                        anime_details['distributor'], anime_details['contentRating'], anime_details['revURL']))
        cnx.commit()
        logger.info("Inserted anime with ID {}".format(anime_details['id']))
        time.sleep(1)
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    populate_review_db()
