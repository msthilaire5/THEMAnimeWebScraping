import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_title
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class get_title_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_can_get_title(self, mock_get):
        review_link = "tests/example_pages/review685.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        title = get_title(review_link)
        expected = ".hack//Legend of the Twilight"
        self.assertEqual(expected, title)
        mock_get.assert_called_with("tests/example_pages/review685.html")

    @patch('requests.get')
    def test_title_missing(self, mock_get):
        review_link = "tests/example_pages/no_title.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        with self.assertRaises(MissingAnimeDetailError):
            title = get_title(review_link)
            mock_get.assert_called_with(review_link)


if __name__ == '__main__':
    unittest.main()
