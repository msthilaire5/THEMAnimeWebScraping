import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_distributor
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class get_distributor_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_distributor_link_present(self, mock_get):
        review_link = "tests/example_pages/review685.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        distributor = get_distributor(review_link)
        expected = "FUNimation"
        self.assertEqual(expected, distributor)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_no_distributor_link(self, mock_get):
        review_link = "tests/example_pages/review1423.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        distributor = get_distributor(review_link)
        expected = "NIS America"
        self.assertEqual(expected, distributor)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_no_distributor_link_and_extra_info(self, mock_get):
        review_link = "tests/example_pages/review593.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        distributor = get_distributor(review_link)
        expected = "Viz"
        self.assertEqual(expected, distributor)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_distributor_missing(self, mock_get):
        review_link = "tests/example_pages/no_distributor.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        with self.assertRaises(MissingAnimeDetailError):
            distributor = get_distributor(review_link)
            mock_get.assert_called_with(review_link)


if __name__ == '__main__':
    unittest.main()
