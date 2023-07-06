import sqlite3
from datetime import date, datetime

from work_with_api import UsdAPI, EuroAPI, EthAPI, BtcAPI
import logging


def get_rates():
    today = date.today()
    con = sqlite3.connect('rates_db.db')
    cur = con.cursor()

    # con.execute("CREATE TABLE RATES (DATE DATE, RATE_USD FLOAT, RATE_EURO FLOAT , RATE_ETH FLOAT , RATE_BTC FLOAT)")

    cur.execute("SELECT * FROM `RATES` ORDER BY DATE DESC;")
    rows = cur.fetchall()

    if rows and datetime.strptime(rows[0][0], '%Y-%m-%d').date() == today:
        logging.info(f"didnt added rates for {today}, already excist: {rows[0]}")
    else:
        cur.execute(f"INSERT INTO `RATES` VALUES ('{today}', '{str(UsdAPI().get_rate())}' , '{str(EuroAPI().get_rate())}', '{str(EthAPI().get_rate())}', '{str(BtcAPI().get_rate())}')")
        con.commit()
        logging.info(f"added rates for {today}")

    return cur


def find_rate(currency=None):
    cur = get_rates()

    if not currency:
        cur.execute("SELECT * FROM `RATES` ORDER BY DATE DESC;")
        return cur.fetchall()[0][1:]

    answer = cur.execute(f"SELECT {'RATE_'+currency.upper()} FROM RATES ")

    return answer.fetchall()[0][0]
