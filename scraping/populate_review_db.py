import requests
import re
from bs4 import BeautifulSoup


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
