import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_AKA
from scraping.MissingAnimeDetailError import MissingAnimeDetailError


class get_AKA_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_can_get_AKA(self, mock_get):
        review_link = "tests/example_pages/review685.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        aka = get_AKA(review_link)
        expected = ".hack//黄昏の腕輪伝説 (hack//Tasogare no Udewa Densetsu), " \
                   ".hack//Legend of the Twilight Bracelet, .hack//LEGEND, .hack//DUSK"
        self.assertEqual(expected, aka)
        mock_get.assert_called_with(review_link)

    @patch('requests.get')
    def test_AKA_missing(self, mock_get):
        review_link = "tests/example_pages/no_aka.html"
        review_page = open(review_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = review_page

        with self.assertRaises(MissingAnimeDetailError):
            title = get_AKA(review_link)
            mock_get.assert_called_with(review_link)


if __name__ == '__main__':
    unittest.main()
