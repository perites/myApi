from flask import Flask, request, jsonify
import logging
import requests
from work_with_db import find_rate
import sqlite3
from datetime import date


app = Flask(__name__)

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='currencyAPI_logs.log', filemode='w', level=logging.DEBUG)


@app.route("/get-rates")
def get_rates():

    tokens = ["aa1", "aa2", "bb1"]

    headers = request.headers
    token = headers.get("Token")
    if token not in tokens:
        logging.info(f"didnt authorised  with token {token}")
        return jsonify({"message": "ERROR: Unauthorized"}), 401

    logging.info(f"authorised sucesfuly with token {token}")
    currency = request.args.get("currency")
    amount = request.args.get("amount")

    logging.info(f"Got {currency} and {amount} , procesing")
    currencys = ["Euro", "Usd",'Eth', "Btc"]
    
    if not currency:    
        answer = find_rate() 
        return jsonify(answer), 200 
    if currency not in currencys:
        return jsonify({"message": "Wrong currency, please check if correct"}), 500
   
    answer = find_rate(currency , currencys)
    if not amount:    
        return jsonify(answer, currency), 200
    
    try:
        amount = float(amount)
        return jsonify(float(answer)*amount, currency), 200

    except Exception as e:
        logging.error(f"Error : {e}")
        return jsonify({"message": "Error happend, please check if amount is a number"}), 500



    



if __name__ == '__main__':
    app.run(debug=True)
