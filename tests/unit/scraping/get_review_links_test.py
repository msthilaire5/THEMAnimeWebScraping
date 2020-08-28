import unittest
from unittest.mock import MagicMock, patch
from scraping.populate_review_db import get_review_links


class get_review_links_TestCase(unittest.TestCase):

    @patch('requests.get')
    def test_a_reviews(self, mock_get):
        a_list_link = "tests/example_pages/a_reviews.html"
        a_reviews = open(a_list_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = a_reviews

        rev_links = get_review_links(a_list_link)
        expected = [
            "viewreview.php?id=685",
            "viewreview.php?id=1",
            "viewreview.php?id=1634",
            "viewreview.php?id=1962",
            "viewreview.php?id=3",
            "viewreview.php?id=1121",
            "viewreview.php?id=2",
            "viewreview.php?id=1442",
            "viewreview.php?id=20",
            "viewreview.php?id=9",
            "viewreview.php?id=8",
            "viewreview.php?id=1934"
        ]
        self.assertCountEqual(rev_links, expected)
        mock_get.assert_called_with(a_list_link)

    @patch('requests.get')
    def test_no_reviews(self, mock_get):
        no_reviews_link = "tests/example_pages/no_reviews.html"
        no_reviews = open(no_reviews_link, "r")
        mock_get.return_value = MagicMock()
        mock_get.return_value.text = no_reviews

        rev_links = get_review_links(no_reviews_link)
        expected = []
        self.assertCountEqual(rev_links, expected)
        mock_get.assert_called_with(no_reviews_link)


if __name__ == '__main__':
    unittest.main()
