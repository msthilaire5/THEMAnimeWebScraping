import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_genre
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class get_genre_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_can_get_genre(self, mock_get):
        review_link = "tests/example_pages/review685.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        genre = get_genre(review_link)
        expected = "Sci-fi with some comedy and fantasy elements"
        self.assertEqual(expected, genre)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_genre_missing(self, mock_get):
        review_link = "tests/example_pages/no_genre.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        with self.assertRaises(MissingAnimeDetailError):
            genre = get_genre(review_link)
            mock_get.assert_called_with(review_link)


if __name__ == '__main__':
    unittest.main()
