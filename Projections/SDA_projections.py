import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#%%

def get_dico(name, carbon_intensity_1, carbon_intensity_2, objectivs):

	dico = {'name':name, 'carbon_intensity_1':carbon_intensity_1, 'carbon_intensity_2':carbon_intensity_2,
	        'objectivs':objectivs}

	return dico

ipsen = get_dico('IPSEN', 79.6, 44.2, -0.06)
lvmh = get_dico('LVMH', 8.58, 4.74, -0.5)
schneider = get_dico('Schneider Electric', 7.69, 4.12, -0.06)
adp = get_dico('Aéroport de Paris', 19.6, 13.36, -0.06)
bouygues = get_dico('Bouygues construction', 79.6, 44.2, -0.06)
pernot_ricard = get_dico('Pernot Ricard', 28, 21, -0.06)

class Company_Analyse():
	#Le scope doit être en tonne de CO2 équivalent par millions de chiffre d'affaire
	def __init__(self, company, oldest_year=2016, last_year = 2022):

		self.name = company['name']
		self.carbon_intensity_1 = company['carbon_intensity_1']
		self.carbon_intensity_2 = company['carbon_intensity_2']
		self.objectivs = company['objectivs']
		self.oldest_year = oldest_year
		self.last_year = last_year

	def carbon_economic_intensity(self):
		#tonne de CO2eq/millions de chiffre d'affaire
		'''print("{} a une intensité carbonne de {} tCO2/millions de chiffre d'affaire "
		      .format(self.name,"%.2f" % (self.carbon_intensity_2)))'''


	def evolution_ci_scope1(self):
		self.carbon_economic_intensity()

		evolution = ((self.carbon_intensity_2/self.carbon_intensity_1)**(1/(self.last_year-self.oldest_year))-1)
		#print("{} réduit ses émissions carbonnes de {} % par an".format(self.name,"%.2f" % evolution))
		return evolution

	def projection(self):
		evolution = self.evolution_ci_scope1()
		time = list(range(self.oldest_year, 2051))
		company_pathway = [self.carbon_intensity_1]
		objectivs_pathway = [self.carbon_intensity_1]

		for i in range(len(time)):
			intensity = company_pathway[-1] * (1 + evolution)
			company_pathway.append(intensity)
			if i < 10 :
				obj = objectivs_pathway[-1]*(1+evolution)
				objectivs_pathway.append(obj)
			else:
				obj = objectivs_pathway[-1] * (1 + self.objectivs)
				objectivs_pathway.append(obj)

		objectivs_pathway.pop(-1)
		company_pathway.pop(-1)
		return time, company_pathway, objectivs_pathway

	def get_df(self):
		time, company_pathway, objectivs = self.projection()

		df = pd.DataFrame({'time':time, self.name+' ojectivs':objectivs, self.name+' historical': company_pathway})

		df.set_index('time', inplace=True, drop=True)

		fig = px.line(df, x=df.index, y=df.columns,
		              title='{} decarbonization pathway'.format(self.name))
		fig.update_xaxes(
			dtick="M1",
			tickformat="%b\n%Y",
			showgrid=False
		)
		fig.update_yaxes(
			showgrid=False
		)

		fig.update_layout(xaxis_title="Years",
		                  yaxis_title="GSE t/eq CO2 per million turnover",
		                  title={
			                  'y': 0.9,
			                  'x': 0.5,
			                  'xanchor': 'center',
			                  'yanchor': 'top'},
		                  legend=dict(
			                  yanchor="top",
			                  y=0.99,
			                  xanchor="left",
			                  x=0.9,
		                  ))
		#fig.show()

		return df

class Portefeuille_extra():

	def __init__(self):
		self.schneider = Company_Analyse(schneider).get_df()
		self.lvmh = Company_Analyse(lvmh).get_df()
		self.ipsen = Company_Analyse(ipsen).get_df()
		self.adp = Company_Analyse(adp).get_df()
		self.bouygues = Company_Analyse(bouygues).get_df()
		self.pernot_ricard = Company_Analyse(pernot_ricard).get_df()


	def mix_pathway(self):

		df = pd.concat([self.schneider['Schneider Electric historical'],(self.lvmh['LVMH historical']),(self.ipsen['IPSEN historical']),(self.adp['Aéroport de Paris historical'])
			,(self.bouygues['Bouygues construction historical']),(self.pernot_ricard['Pernot Ricard historical'])], axis=1)

		df['Fund obj'] = df[df.columns[~df.columns.str.contains('objectivs')]].sum(axis=1)

		df['Fund pathway'] = df[df.columns[~df.columns.str.contains('historical')]].sum(axis=1)
		print(df['Fund pathway'])
		df = df['Fund pathway']
		fig = px.line(df, x=df.index, y=df,
		              title='Fund decarbonization pathway')
		fig.update_xaxes(
			dtick="M1",
			tickformat="%b\n%Y",
			showgrid=False
		)
		fig.update_yaxes(
			showgrid=False
		)

		fig.update_layout(xaxis_title="Years",
		                  yaxis_title="GSE t/eq CO2 per million turnover",
		                  title={
			                  'y': 0.9,
			                  'x': 0.5,
			                  'xanchor': 'center',
			                  'yanchor': 'top'},
		                  legend=dict(
			                  yanchor="top",
			                  y=0.99,
			                  xanchor="left",
			                  x=0.9,
		                  ))
		fig.show()


a = Portefeuille_extra()
a.mix_pathway()




















