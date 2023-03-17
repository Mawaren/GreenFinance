import sqlite3
import yfinance as yf
import pandas as pd

class get_hist():

	def __init__(self):
		self.ticker = {'^FCHI':'CAC40', 'MC.PA':'LVMH',
		               'IPN.PA':'IPSEN', 'SU.PA':'SE', 'ADP.PA':'ADP','EN.PA':'Bouygues', 'RI.PA': 'Pernot Ricard'}
		self.conn = sqlite3.connect('db.sqlite3')

	def get_data(self):
		for key, value in self.ticker.items():
			ticker = yf.Ticker(key)
			hist = ticker.history(period='10y', interval='3mo')
			hist.to_sql(value, self.conn, if_exists='replace')

	def from_sql(self):
		df = pd.read_sql(self.conn, self.ticker)
		return df


a = get_hist()
a.get_data()