import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_length_info
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class get_length_info_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_not_movie(self, mock_get):
        review_link = "tests/example_pages/review685.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        length_info = get_length_info(review_link)
        expected = ("Television series", 12, 23)
        self.assertCountEqual(expected, length_info)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_one_unit_movie(self, mock_get):
        review_link = "tests/example_pages/review593.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        length_info = get_length_info(review_link)
        expected = ("Movie", 1, 78)
        self.assertCountEqual(expected, length_info)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_length_missing(self, mock_get):
        review_link = "tests/example_pages/no_length.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        with self.assertRaises(MissingAnimeDetailError):
            length_info = get_length_info(review_link)
            mock_get.assert_called_with(review_link)


if __name__ == '__main__':
    unittest.main()
