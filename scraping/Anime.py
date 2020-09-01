import re
import string
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class Anime:

    def __init__(self, review_url, review_soup):
        title_tag = review_soup.find('h1')
        aka_tag = review_soup.find('b', text=re.compile("AKA"))
        genre_tag = review_soup.find('b', text=re.compile("Genre"))
        length_tag = review_soup.find('b', text=re.compile("Length"))
        distributor_tag = review_soup.find('b', text=re.compile("Distributor"))
        cr_tag = review_soup.find('b', text=re.compile("Content Rating"))

        self.anime_id = self._get_id(review_url)
        self.title = self._get_title(title_tag)
        self.aka = self._get_aka(aka_tag)
        self.genre = self._get_genre(genre_tag)
        self.media_type, self.num_episodes, self.mins_per_episode = self._get_length_info(length_tag)
        self.distributor = self._get_distributor(distributor_tag)
        self.content_rating = self._get_content_rating(cr_tag)
        self.url = review_url

    @staticmethod
    def _get_id(review_url):
        id_idx = review_url.find('=') + 1
        return int(review_url[id_idx:])

    @staticmethod
    def _get_title(title_tag):
        try:
            return title_tag.text
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing a title.")

    @staticmethod
    def _get_aka(aka_tag):
        try:
            return aka_tag.next_sibling.strip()
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing alternative names.")

    @staticmethod
    def _get_genre(genre_tag):
        try:
            return genre_tag.next_sibling.strip()
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its genre.")

    @staticmethod
    def _get_length_info(length_tag):
        try:
            length_details = length_tag.next_sibling.split(",")
            media_type = length_details[0].strip()
            num_episodes = 1 if len(length_details) < 3 else int(length_details[1].split()[0])
            mins_per_episode = int(length_details[-1].split()[0])
            return media_type, num_episodes, mins_per_episode
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its length information.")

    @staticmethod
    def _get_distributor(distributor_tag):
        try:
            distributor_link = distributor_tag.find_next_sibling('a')
            if distributor_link:
                distributor = distributor_link.string
            else:
                distributor_details = distributor_tag.next_sibling
                by_location = distributor_details.find("by")
                distributor_start = by_location + len("by ")
                delimiters = "[{}]".format(string.punctuation)
                distributor = re.split(delimiters, distributor_details[distributor_start:])[0]
            return distributor
        except AttributeError:
            raise MissingAnimeDetailError("This anime's review is missing its distributor.")

    @staticmethod
    def _get_content_rating(cr_tag):
        try:
            content_rating = cr_tag.next_sibling
            if "(" in content_rating:
                explanation_start = content_rating.find("(")
                content_rating = content_rating[:explanation_start]
            return content_rating.strip()
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
