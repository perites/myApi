from flask import Flask, request, jsonify
from apiClasses_api import *
import logging


app = Flask(__name__)

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='currencyAPI_logs.log', filemode='w', level=logging.DEBUG)


@app.route("/get-rates")
def get_rates():
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
                return "Error happend, please check if amount is a number"

        return jsonify(answer, currency), 200

    elif currency and currency not in currencys:
        return "Wrong currency, please check if correct"

    else:
        answer = [n for n in currencys.values()]
        return jsonify(answer), 200


if __name__ == '__main__':
    app.run(debug=True)
