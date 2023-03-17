import sqlite3
import plotly.express as px
import pandas as pd

tickers = ['LVMH', 'IPSEN','SE', 'ADP', 'Bouygues', 'Pernot Ricard', 'CAC40']
part = [0.15, 0.15, 0.15, 0.15, 0.15, 0.25]
class perf():
	def __init__(self, tickers):
		self.conn = sqlite3.connect('db.sqlite3')
		self.tickers = tickers

	def get_data(self):
		historique = pd.DataFrame(columns=self.tickers)
		for i in self.tickers:

			histo = pd.read_sql_query("SELECT DATE, CLOSE FROM '{}'".format(i), self.conn)
			historique[i] = histo['Close']
			date = histo['Date']

		historique.index = date

		return historique

	def get_histor(self):

		historique = self.get_data()

		#historique.iloc[:, :-1] = historique.iloc[:, :-1] * part

		histor = ((historique/historique.iloc[0])*100)

		histor = histor[histor.index.str.contains('-03-')]

		return histor

	def pourcentage_changement(self):
		histor = self.get_histor()

		histor.index= [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

		fig = px.line(histor, x=histor.index, y=histor.columns,

		              title='custom tick labels')
		fig.update_xaxes(
			dtick="M1",
			tickformat="%b\n%Y")
		fig.show()

	def camembert(self):

		df = pd.DataFrame(tickers[:-1], part)
		fig = px.pie(df, values=df.index, names=0)
		fig.show()

	def total(self):
		histor = self.get_histor()

		histor['Wallet'] = histor.iloc[:,:-1].sum(axis=1)
		histor['Wallet'] = histor['Wallet']/6
		histor.index = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

		evolution2 = ((histor.iloc[-1] / histor.iloc[0]) ** (1 / (2023 - 2013)) - 1)


		histor = histor[['CAC40', 'Wallet']]
		evolution = ((histor.iloc[-1]/histor.iloc[0])**(1/(2023-2013))-1)

		time = list(range(2013, 2031))
		company_pathway = [histor.iloc[0][0]]

		cac_patwhay = [histor.iloc[0][1]]

		for i in range(len(time)):
			intensity = company_pathway[-1] * (1 + evolution[1])
			intensity_2 = cac_patwhay[-1] * (1 + evolution[0])
			company_pathway.append(intensity)
			cac_patwhay.append(intensity_2)
		company_pathway.pop(-1)
		cac_patwhay.pop(-1)

		df = pd.DataFrame({'time': time, 'net 0 fund': company_pathway, 'cac40':cac_patwhay})

		df.set_index('time', inplace=True, drop=True)

		fig = px.line(df, x=df.index, y=df.columns,
		              title='Net 0 fund and cac40 forecast based on historical annual return')
		fig.update_xaxes(
			dtick="M1",
			tickformat="%b\n%Y",
			showgrid=False
		)
		fig.update_yaxes(
			showgrid=False
		)

		fig.update_layout(xaxis_title="Years",
			yaxis_title="Stock evolution",
			 title={
          'y': 0.85,
          'x': 0.5,
          'xanchor': 'center',
          'yanchor': 'top'},
		legend=dict(
			yanchor="top",
			y=0.99,
			xanchor="left",
			x=0.01,
		))
		fig.show()

		#print(df)
		return histor
	def graph(self):
		#self.pourcentage_changement()
		#self.camembert()
		histor = self.total()
		fig = px.line(histor, x=histor.index, y=histor.columns,
		              title='Net 0 Fund forecasting')
		fig.update_xaxes(
			dtick="M1",
			tickformat="%b\n%Y",
		)


		fig.show()

a = perf(tickers)
a.graph()

