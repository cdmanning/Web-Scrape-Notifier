import unittest
import requests
from scrape import check_stock, load_config
from unittest.mock import patch, mock_open, MagicMock

class TestScrape(unittest.TestCase):

    def setUp(self):
        self.target = {
            "name": "Test Site",
            "url": "https://test.com",
            "element_tag": "div",
            "element_class": "inventory",
            "target_text": "Sold Out",
        }

    @patch("scrape.requests.get")
    def test_check_stock_positive_match(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = (
            '<html><body><div class="inventory">In Stock Now!</div></body></html>'
        )
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        result = check_stock(self.target)
        self.assertIsNotNone(result)
        self.assertIn("Alert triggered for: Test Site", result)

    @patch("scrape.requests.get")
    def test_check_stock_negative_match(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = (
            '<html><body><div class="inventory">Status: Sold Out</div></body></html>'
        )
        mock_get.return_value = mock_response
        result = check_stock(self.target)
        self.assertIsNone(result)

    @patch("scrape.requests.get")
    def test_check_stock_network_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        result = check_stock(self.target)
        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open)
    @patch("scrape.json.load")
    def test_load_config(self, mock_json_load, mock_open):
        mock_json_load.return_value = {"targets": [{"name": "Mock", "url": "mock.com"}]}
        config = load_config("dummy_path.json")
        self.assertIn("targets", config)
        self.assertEqual(config["targets"][0]["name"], "Mock")
        mock_open.assert_called_once_with("dummy_path.json", "r")
        mock_json_load.assert_called_once()


if __name__ == "__main__":
    unittest.main()