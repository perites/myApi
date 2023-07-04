

import unittest
import my_api
from unittest import mock
import requests

class TestCurrencyRates(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/get-rates"

    def setUp(self):
        self.headers = {"Token": "aa1"}

    def test_get_all_rates(self):
        response = requests.get(self.base_url, headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 4)

    def test_get_rates_for_usd(self):
        response = requests.get(
            self.base_url + "?currency=Usd", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_get_rates_for_btc(self):
        response = requests.get(
            self.base_url + "?currency=Btc", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)

    @mock.patch('my_api.requests.get')
    def test_convert_euro_to_hrn(self , mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '40.05000', 'sale': '41'}, {
            'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '36.75000', 'sale': '37.25000'}] # Simulated response from the API
        mock_get.return_value = mock_response

        # Call the route under test
        with my_api.app.test_client() as client:
            response = client.get(
                self.base_url + "?currency=Euro&amount=10", headers=self.headers)

        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0], 41*10)

    @mock.patch('my_api.requests.get')
    def test_convert_euro_to_hrn_with_different_amount(self, mock_get):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '40.05000', 'sale': '41'}, {
            'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '36.75000', 'sale': '37.25000'}]  # Simulated response from the API
        mock_get.return_value = mock_response

        # Call the route under test
        with my_api.app.test_client() as client:
            response = client.get(
                self.base_url + "?currency=Euro&amount=20", headers=self.headers)

        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0], 41*20)

    def test_invalid_currency(self):
        response = requests.get(
            self.base_url + "?currency=Usff", headers=self.headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 500)

    def test_invalid_amount(self):
        response = requests.get(
            self.base_url + "?currency=Euro&amount=ff", headers=self.headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 500)

    def test_unauthorized_access(self):
        response = requests.get(self.base_url + "?currency=Euro&amount=20")
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data["message"], "ERROR: Unauthorized")

    def test_unauthorized_access_with_different_token(self):
        headers = {"Token": "cc2"}
        response = requests.get(
            self.base_url + "?currency=Usff", headers=headers
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data["message"], "ERROR: Unauthorized")


if __name__ == "__main__":
    unittest.main()


