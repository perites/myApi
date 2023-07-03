import requests
import json 

headers = {"Token" : "aa1"}

test1 = requests.get("http://127.0.0.1:5000/get-rates", headers=headers)
test2 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usd", headers=headers)
test3 = requests.get("http://127.0.0.1:5000/get-rates?currency=Btc", headers=headers)
test4 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=10", headers=headers)
test5 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=20", headers=headers)
test6 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usff", headers=headers)
test7 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=ff", headers=headers)

test8 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=20")
headers = {"Token" : "cc2" } 
test9 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usff", headers=headers)



print(test1.json(), "--test1", "expected : 4 rates")
print(test2.json(), "--test2", "expected : 1 rate for Usd")
print(test3.json(), "--test3", "expected : 1 rate for Btc")
print(test4.json(), "--test4", "expected : 10 euros in hrn")
print(test5.json(), "--test5", "expected : 20 euros in hrn")
print(test6.json(), "--test6", "expected : 'Wrong currency, please check if correct'")
print(test7.json(), "--test7", "expected : 'Error happend, please check if amount is a number'")
print(test8.json(), "--test8", "expected : 'message: ERROR: Unauthorized'")
print(test9.json(), "--test9", "expected : 'message: ERROR: Unauthorized'")