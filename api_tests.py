# from flask import Flask, jsonify
# import unittest


# import json

# headers = {"Token" : "aa1"}

# test1 = requests.get("http://127.0.0.1:5000/get-rates", headers=headers)
# test2 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usd", headers=headers)
# test3 = requests.get("http://127.0.0.1:5000/get-rates?currency=Btc", headers=headers)
# test4 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=10", headers=headers)
# test5 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=20", headers=headers)
# test6 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usff", headers=headers)
# test7 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=ff", headers=headers)

# test8 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=20")
# headers = {"Token" : "cc2" }
# test9 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usff", headers=headers)


# print(test1.json(), "--test1", "expected : 4 rates")
# print(test2.json(), "--test2", "expected : 1 rate for Usd")
# print(test3.json(), "--test3", "expected : 1 rate for Btc")
# print(test4.json(), "--test4", "expected : 10 euros in hrn")
# print(test5.json(), "--test5", "expected : 20 euros in hrn")
# print(test6.json(), "--test6", "expected : 'Wrong currency, please check if correct'")
# print(test7.json(), "--test7", "expected : 'Error happend, please check if amount is a number'")
# print(test8.json(), "--test8", "expected : 'message: ERROR: Unauthorized'")
# print(test9.json(), "--test9", "expected : 'message: ERROR: Unauthorized'")





# class ApiTest(unittest.TestCase):
# 	def test_just_api(self):

# 		fake_resp = mocker.Mock()
# 		fake_resp.json = mocker.Mock(return_value=[41.1, 37.25,75989.37223832252,1225308.6921476214])
# 		fake_resp.status_code = HTTPStatus.OK
# 		mocker.patch("requests.get", return_value=fake_resp)

# 		headers = {"Token" : "aa1"}
# 		result = requests.get("http://127.0.0.1:5000/get-rates", headers=headers).json()
# 		self.assertEqual(result,[41.1, 37.25,75989.37223832252,1225308.6921476214])


# import unittest
# import requests

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

        # print(response, "p1")
        # print(response.json(), "p2")
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0], 41*10)

        mock_get.assert_called_once_with(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")


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

        # mock_get.assert_called_once_with(
        #     "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")

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


# import unittest
# import requests
# from unittest import mock


# class TestCurrencyRates(unittest.TestCase):
#     base_url = "http://127.0.0.1:5000/get-rates"

#     def setUp(self):
#         self.headers = {"Token": "aa1"}

#     @mock.patch("requests.get")
#     def test_convert_euro_to_hrn(self, mock_get):
#         # Create a mock response
#         mock_response = mock.Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = [{'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '40.05000', 'sale': '41.05000'}, {'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '36.75000', 'sale': '37.25000'}]

#         # Configure the mock get method to return the mock response
#         mock_get.return_value = mock_response

#         # Make the request
#         response = requests.get(
#             self.base_url + "?currency=Euro", headers=self.headers
#         )

#         # Assert the response
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), "41.05")

#         # Assert that the mock get method was called with the correct arguments
#         mock_get.assert_called_once_with(
#             self.base_url + "?currency=Euro", headers=self.headers
#         )


# if __name__ == "__main__":
#     unittest.main()


# replace with the module name where your Flask app resides

# def math_with_api():
#     response = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")
#     a = response[0] + 10
#     b = response[1] + 20
#     return a, b

# class TestMathWithAPI(unittest.TestCase):

# 	@mock.patch('requests.get')
# 	def test_math(self, mock_get):
# 		mock_response = mock.Mock()
# 		mock_response.status_code = 200
# 		mock_response.json.return_value = [30, 40]
# 		mock_get.return_value = mock_response

# 		# Call the route under test
# 		with exceptions.app.test_client() as client:
# 		    response = client.get('/')

# 		# Assert the expected status code and JSON response
# 		self.assertEqual(response.status_code, 200)
# 		self.assertEqual(response.json, {'a': 40, 'b': 60})  # Expected values after performing math operations

# 		# Assert that the API was called with the correct parameters
# 		mock_get.assert_called_once_with('http://127.0.0.1:5000/')


# if __name__ == '__main__':
#     unittest.main()


# # class TestMathWithAPI(unittest.TestCase):
#    @mock.patch('exceptions.requests.get')
# #     def test_math(self, mock_get):
# #         # Configure the mock response
#        mock_response = mock.Mock()
#         mock_response.status_code = 200
#         # Simulated response from the API
#         mock_response.json.return_value = [20, 30]
#         mock_get.return_value = mock_response

#         # Call the route under test
#         with exceptions.app.test_client() as client:
#             response = client.get('/')

#         # Assert the expected status code and JSON response
#         self.assertEqual(response.status_code, 200)
#         # Expected values after performing math operations
#         self.assertEqual(response.json, [30, 50])

#         # Assert that the API was called with the correct parameters
#         mock_get.assert_called_once_with(
#             "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")

# # if __name__ == '__main__':
# #     unittest.main()


# [{'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '40.05000', 'sale': '41.05000'}, {
#     'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '36.75000', 'sale': '37.25000'}]
