import requests
from exceptions import *
import json


def get_response_for_crypto():
    url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD'
    headers = {'X-CoinAPI-Key': "8FBF51F8-332B-416E-A836-4603D4B21753"}
    response_for_eth = requests.get(url, headers=headers)
    if not response_for_eth.status_code == 200:
        raise BadAPIResponse

    url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD'
    headers = {'X-CoinAPI-Key': "8FBF51F8-332B-416E-A836-4603D4B21753"}
    response_for_btc = requests.get(url, headers=headers)
    if not response_for_btc.status_code == 200:
        raise BadAPIResponse

    return [response_for_btc.json(), response_for_eth.json()]


def write_response():
    response = get_response_for_crypto()
    with open("response.json", "w") as write_file:
        json.dump(response, write_file)
