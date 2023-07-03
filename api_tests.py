
# import json 
# import requests
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


# import unittest
# import my_api

# import unittest.mock



# class ApiTest(unittest.TestCase):
# 	def test_just_api(self):

# 		fake_resp = mocker.Mock()
# 		fake_resp.json = mocker.Mock(return_value=[41.1, 37.25,75989.37223832252,1225308.6921476214])
# 		fake_resp.status_code = HTTPStatus.OK
# 		mocker.patch("requests.get", return_value=fake_resp)

# 		headers = {"Token" : "aa1"}
# 		result = requests.get("http://127.0.0.1:5000/get-rates", headers=headers).json()
# 		self.assertEqual(result,[41.1, 37.25,75989.37223832252,1225308.6921476214])








#ChatGPt:


import unittest
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
        response = requests.get(self.base_url + "?currency=Usd", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_get_rates_for_btc(self):
        response = requests.get(self.base_url + "?currency=Btc", headers=self.headers)
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_convert_euro_to_hrn(self):
        response = requests.get(
            self.base_url + "?currency=Euro&amount=10", headers=self.headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_convert_euro_to_hrn_with_different_amount(self):
        response = requests.get(
            self.base_url + "?currency=Euro&amount=20", headers=self.headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)

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
