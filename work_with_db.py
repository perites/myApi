import sqlite3
from datetime import date, datetime

from work_with_api import UsdAPI, EuroAPI, EthAPI, BtcAPI
import logging


def get_rates():
    today = date.today()
    con = sqlite3.connect('rates_db.db')
    cur = con.cursor()

    # con.execute("CREATE TABLE 'RATES' ('DATE' DATE, 'RATE_USD' FLOAT, 'RATE_EURO' FLOAT , 'RATE_ETH' FLOAT , 'RATE_BTC' FLOAT)")

    cur.execute("SELECT * FROM `RATES` ORDER BY DATE DESC;" ) 
    rows = cur.fetchall()

    if rows and datetime.strptime(rows[0][0], '%Y-%m-%d').date() == today:
        logging.info(f"didnt added rates for {today}, already excist: {rows[0]}")
    else:
        cur.execute(f"INSERT INTO `RATES` VALUES ('{today}', '{str(EuroAPI().get_rate())}' , '{str(UsdAPI().get_rate())}', '{str(EthAPI().get_rate())}', '{str(BtcAPI().get_rate())}')")
        con.commit()
        logging.info(f"added rates for {today}")
        cur.execute("SELECT * FROM `RATES`")
        rows = cur.fetchall()
        con.close()

    return rows


def find_rate(currency=None):
    rows = get_rates()
    if not currency:
        return rows[0][1:]

    d = {"Euro": 1,
         "Usd": 2,
         "Eth": 3,
         "Btc": 4}
    return rows[0][d[currency]]
