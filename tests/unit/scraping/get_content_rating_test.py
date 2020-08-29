import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_content_rating
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class get_content_rating_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_can_get_rating(self, mock_get):
        review_link = "tests/example_pages/review685.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        rating = get_content_rating(review_link)
        expected = "13+"
        self.assertEqual(expected, rating)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_rating_with_no_explanation(self, mock_get):
        review_link = "tests/example_pages/no_cr_explanation.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        rating = get_content_rating(review_link)
        expected = "PG"
        self.assertEqual(expected, rating)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_rating_missing(self, mock_get):
        review_link = "tests/example_pages/no_content_rating.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        with self.assertRaises(MissingAnimeDetailError):
            rating = get_content_rating(review_link)
            mock_get.assert_called_with(review_link)


if __name__ == '__main__':
    unittest.main()
