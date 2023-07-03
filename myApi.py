from flask import Flask, request, jsonify

import sys
sys.path.append(
    'C://Users//nikit//OneDrive//Documents//pyfile//pyLearning//currencyAPI')
from apiClasses import *


app = Flask(__name__)


@app.route("/get-rates")
def get_rates():
    currency = request.args.get("currency")
    amount = request.args.get("amount")

    currencys = ["Usd", "Euro", "Eth",  "Btc"]
    if currency and currency in currencys:
        answer = get_rate_api(currency)

        if amount:
            try:
                amount = float(amount)
                return jsonify([answer[0]*amount, currency])

            except Exception as e:
                print(e)

        return jsonify(answer), 200

    else:
        return jsonify(get_rate_api()), 200


def get_rate_api(currency=None):
    if currency:
        if currency == "Usd":
            return UsdAPI().get_rate()
        if currency == "Euro":
            return EuroAPI().get_rate()
        if currency == "Eth":
            return EthAPI().get_rate()
        if currency == "Btc":
            return BtcAPI().get_rate()
    else:
        return [BtcAPI().get_rate(), EthAPI().get_rate(), EuroAPI().get_rate(), UsdAPI().get_rate()]


if __name__ == '__main__':
    app.run(debug=True)
