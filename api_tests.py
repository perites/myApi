import requests
import json 


test1 = requests.get("http://127.0.0.1:5000/get-rates")
test2 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usd")
test3 = requests.get("http://127.0.0.1:5000/get-rates?currency=Btc")
test4 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=10")
test5 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=20")
test6 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usff")
test7 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=ff")

print(test1.json(), "--test1", "expected : 4 rates")
print(test2.json(), "--test2", "expected : 1 rate for Usd")
print(test3.json(), "--test3", "expected : 1 rate for Btc")
print(test4.json(), "--test4", "expected : 10 euros in hrn")
print(test5.json(), "--test5", "expected : 20 euros in hrn")

# як виводити саме напис ? 
print(test6, "--test6", "expected : 'Wrong currency, please check if correct'")
print(test7, "--test7", "expected : 'Error happend, please check if amount is a number'")