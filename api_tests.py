import requests
import json 


test1 = requests.get("http://127.0.0.1:5000/get-rates")
test2 = requests.get("http://127.0.0.1:5000/get-rates?currency=Usd")
test3 = requests.get("http://127.0.0.1:5000/get-rates?currency=Btc")
test4 = requests.get("http://127.0.0.1:5000/get-rates?currency=Euro&amount=36")
test5 = requests.get("http://127.0.0.1:5000/get-rates?currency=Eth&amount=34")


print(test1.json(), "--test1")
print(test2.json(), "--test2")
print(test3.json(), "--test3")
print(test4.json(), "--test4")
print(test5.json(), "--test5")
