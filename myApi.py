from flask import Flask, request, jsonify
from apiClasses_api import *
import logging


app = Flask(__name__)

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='currencyAPI_logs.log', filemode='w', level=logging.DEBUG)


@app.route("/get-rates")
def get_rates():

    tokens=["aa1", "aa2", "bb1"]


    headers = request.headers
    token = headers.get("Token")
    if token in tokens:
        logging.info(f"authorised sucesfuly with token {token}")
        currency = request.args.get("currency")
        amount = request.args.get("amount")

        currencys = {"Usd":  UsdAPI().get_rate(),
                     "Euro": EuroAPI().get_rate(),
                     "Eth": EthAPI().get_rate(),
                     "Btc": BtcAPI().get_rate()}

        logging.info(f"Got {currency} and {amount} , procesing")
        if currency and currency in currencys:
            answer = currencys[currency]
            if amount:
                try:
                    amount = float(amount)
                    return jsonify(answer*amount, currency), 200

                except Exception as e:
                    logging.error(f"Error : {e}")
                    return jsonify({"message":"Error happend, please check if amount is a number"}), 500

            return jsonify(answer, currency), 200

        elif currency and currency not in currencys:
            return jsonify({"message":"Wrong currency, please check if correct"}), 500

        else:
            answer = [n for n in currencys.values()]
            return jsonify(answer), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True)
