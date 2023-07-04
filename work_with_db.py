import sqlite3
from datetime import date

from work_with_api import UsdAPI , EuroAPI, EthAPI, BtcAPI
import logging


def get_rates():
	today = date.today()
	con = sqlite3.connect('apiDB.db')
	cur = con.cursor()

	# con.execute("CREATE TABLE 'RATES' ('DATE' DATE, 'RATE_USD' STRING, 'RATE_EURO' STRING , 'RATE_ETH' STRING , 'RATE_BTC' STRING)")



	cur.execute("SELECT * FROM `RATES`")
	rows = cur.fetchall()


	if rows and rows[-1][0] == str(today):
		logging.info(f"didnt added rates for {today}, already excist: {rows}")
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
	print(rows)
	if not currency:
		return rows[-1][1:]

	d = {"Euro" : 1, 
		 "Usd": 2, 
		"Eth" : 3 , 
		"Btc": 4}
	return rows[-1][d[currency]]
    	



