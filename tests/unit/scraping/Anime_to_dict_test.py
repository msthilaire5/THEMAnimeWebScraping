import unittest
from bs4 import BeautifulSoup
from scraping.Anime import Anime
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class Anime_to_dict_TestCase(unittest.TestCase):

    def test_all_details_present(self):
        review_link = "tests/example_pages/review685.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=685", review_soup)

        expected = {
            'id': 685,
            'title': ".hack//Legend of the Twilight",
            'aka': ".hack//黄昏の腕輪伝説 (hack//Tasogare no Udewa Densetsu), .hack//Legend of the Twilight Bracelet, "
                   ".hack//LEGEND, .hack//DUSK",
            'genre': "Sci-fi with some comedy and fantasy elements",
            'mediaType': "Television series",
            'numEpisodes': 12,
            'minsPerEpisode': 23,
            'distributor': "FUNimation",
            'contentRating': "13+",
            'revURL': "=685"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_one_unit_movie(self):
        review_link = "tests/example_pages/review593.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=593", review_soup)

        expected = {
            'id': 593,
            'title': "Inuyasha Movie 2: The Castle Beyond the Looking Glass",
            'aka': "犬夜叉 鏡の中の夢幻城 (Inuyasha: Kagami no Naka no Mugenjou)",
            'genre': "Historical fantasy adventure",
            'mediaType': "Movie",
            'numEpisodes': 1,
            'minsPerEpisode': 78,
            'distributor': "Viz",
            'contentRating': "13+",
            'revURL': "=593"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_no_distributor_link(self):
        review_link = "tests/example_pages/review1423.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=1423", review_soup)

        expected = {
            'id': 1423,
            'title': "Kimi ni Todoke (From Me to You) Season 1 Part 1",
            'aka': "君に届け (Japanese)",
            'genre': "Romantic comedy",
            'mediaType': "Television series",
            'numEpisodes': 12,
            'minsPerEpisode': 24,
            'distributor': "NIS America",
            'contentRating': "15+",
            'revURL': "=1423"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_rating_with_no_explanation(self):
        review_link = "tests/example_pages/review1.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=1", review_soup)

        expected = {
            'id': 1,
            'title': ".hack//SIGN",
            'aka': "N/A",
            'genre': "Science-fiction suspense / fantasy adventure",
            'mediaType': "Television series",
            'numEpisodes': 26,
            'minsPerEpisode': 25,
            'distributor': "FUNimation",
            'contentRating': "PG",
            'revURL': "=1"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_duration_range_no_distributor_link(self):
        review_link = "tests/example_pages/review1121.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=1121", review_soup)

        expected = {
            'id': 1121,
            'title': "3x3 Eyes 1&2",
            'aka': "サザンアイ (Sazan Eyes)",
            'genre': "Supernatural horror",
            'mediaType': "OAV series",
            'numEpisodes': 7,
            'minsPerEpisode': 30,
            'distributor': "Pioneer",
            'contentRating': "16+",
            'revURL': "=1121"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_streaming_distributor_no_link(self):
        review_link = "tests/example_pages/review1924.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=1924", review_soup)

        expected = {
            'id': 1924,
            'title': "Abunai Sisters: Koko & Mika",
            'aka': "N/A",
            'genre': "Action comedy",
            'mediaType': "Television series",
            'numEpisodes': 10,
            'minsPerEpisode': 3,
            'distributor': "Crunchyroll",
            'contentRating': "16+",
            'revURL': "=1924"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_about_duration(self):
        review_link = "tests/example_pages/review1717.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")
        anime = Anime("=1717", review_soup)

        expected = {
            'id': 1717,
            'title': "After School of the Earth",
            'aka': "地球の放課後 (Chikyuu no Houkago)",
            'genre': "Sci-Fi (With Some Harem Touches)",
            'mediaType': "Television series",
            'numEpisodes': 9,
            'minsPerEpisode': 11,
            'distributor': "unlicensed",
            'contentRating': "PG-13",
            'revURL': "=1717"
        }
        self.assertDictEqual(anime.to_dict(), expected)

    def test_title_missing(self):
        review_link = "tests/example_pages/no_title.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")

        with self.assertRaises(MissingAnimeDetailError):
            anime = Anime("=685", review_soup)

    def test_aka_missing(self):
        review_link = "tests/example_pages/no_aka.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")

        with self.assertRaises(MissingAnimeDetailError):
            anime = Anime("=685", review_soup)

    def test_genre_missing(self):
        review_link = "tests/example_pages/no_genre.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")

        with self.assertRaises(MissingAnimeDetailError):
            anime = Anime("=685", review_soup)

    def test_length_missing(self):
        review_link = "tests/example_pages/no_length.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")

        with self.assertRaises(MissingAnimeDetailError):
            anime = Anime("=685", review_soup)

    def test_distributor_missing(self):
        review_link = "tests/example_pages/no_distributor.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")

        with self.assertRaises(MissingAnimeDetailError):
            anime = Anime("=685", review_soup)

    def test_rating_missing(self):
        review_link = "tests/example_pages/no_content_rating.html"
        review_html = open(review_link, "r")
        review_soup = BeautifulSoup(review_html, "html.parser")

        with self.assertRaises(MissingAnimeDetailError):
            anime = Anime("=685", review_soup)


if __name__ == '__main__':
    unittest.main()
