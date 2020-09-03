import re
import string
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class Anime:

    def __init__(self, review_url, review_soup):
        self.anime_id = None
        self.title = None
        self.aka = None
        self.genre = None
        self.media_type = None
        self.num_episodes = None
        self.mins_per_episode = None
        self.distributor = None
        self.content_rating = None

        title_tag = review_soup.find('h1')
        aka_tag = review_soup.find('b', text=re.compile("AKA"))
        genre_tag = review_soup.find('b', text=re.compile("Genre"))
        length_tag = review_soup.find('b', text=re.compile("Length"))
        distributor_tag = review_soup.find('b', text=re.compile("Distributor"))
        cr_tag = review_soup.find('b', text=re.compile("Content Rating"))

        self._set_id(review_url)
        self._set_title(title_tag)
        self._set_aka(aka_tag)
        self._set_genre(genre_tag)
        self._set_length_info(length_tag)
        self._set_distributor(distributor_tag)
        self._set_content_rating(cr_tag)
        self.url = review_url

    def _set_id(self, review_url):
        id_idx = review_url.find('=') + 1
        self.anime_id = int(review_url[id_idx:])

    def _set_title(self, title_tag):
        try:
            self.title = title_tag.text
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing a title.")

    def _set_aka(self, aka_tag):
        try:
            self.aka = aka_tag.next_sibling.strip()
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing alternative names.")

    def _set_genre(self, genre_tag):
        try:
            self.genre = genre_tag.next_sibling.strip()
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its genre.")

    def _set_length_info(self, length_tag):
        try:
            length_details = length_tag.next_sibling.split(",")
            self.media_type = length_details[0].strip()
            self.num_episodes = 1 if len(length_details) < 3 else int(length_details[1].split()[0])
            ep_length_details = length_details[-1].split()
            if ep_length_details[0].isnumeric():
                mins_per_episode = int(ep_length_details[0])
            elif "-" in ep_length_details[0]:
                mins_per_episode = int(ep_length_details[0].split("-")[0])
            else:
                mins_per_episode = int(ep_length_details[1])
            self.mins_per_episode = mins_per_episode
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its length information.")

    def _set_distributor(self, distributor_tag):
        try:
            distributor_link = distributor_tag.find_next_sibling('a')
            if distributor_link:
                self.distributor = distributor_link.string
            else:
                distributor_details = distributor_tag.next_sibling
                by_location = distributor_details.find("by")
                from_location = distributor_details.find("from")
                on_location = distributor_details.find("on")
                if by_location > -1:
                    distributor_start = by_location + len("by ")
                elif from_location > -1:
                    distributor_start = from_location + len("from ")
                else:
                    distributor_start = on_location + len("on ")
                delimiters = "[{}]".format(string.punctuation)
                self.distributor = re.split(delimiters, distributor_details[distributor_start:])[0]
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its distributor.")

    def _set_content_rating(self, cr_tag):
        try:
            content_rating = cr_tag.next_sibling
            if "(" in content_rating:
                explanation_start = content_rating.find("(")
                content_rating = content_rating[:explanation_start]
            self.content_rating = content_rating.strip()
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its content rating.")

    def to_dict(self):
        return {
            'id': self.anime_id,
            'title': self.title,
            'aka': self.aka,
            'genre': self.genre,
            'mediaType': self.media_type,
            'numEpisodes': self.num_episodes,
            'minsPerEpisode': self.mins_per_episode,
            'distributor': self.distributor,
            'contentRating': self.content_rating,
            'revURL': self.url
        }
