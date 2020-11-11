# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 18:23:02 2020

@author: adria
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader import data as wb
import numpy as np

#Obtenemos data por separado
merval = wb.DataReader('^MERV', 'yahoo', start='2010-01-01')
bovespa = wb.DataReader('^BVSP', 'yahoo', start='2010-01-01')
sp500 = wb.DataReader('^GSPC', 'yahoo', start='2010-01-01')
dow = wb.DataReader('^DJI', 'yahoo', start='2010-01-01')
nasdaq = wb.DataReader('^IXIC', 'yahoo', start='2010-01-01')
vix = wb.DataReader('^VIX', 'yahoo', start='2010-01-01')

#Concatenamos data
indice = pd.concat([merval['Adj Close'], bovespa['Adj Close'], sp500['Adj Close'], dow['Adj Close'], nasdaq['Adj Close'], vix['Adj Close']], axis=1)
indice = indice.sort_values('Date', ascending=True)
indice.columns = ["MERVAL", "BOVESPA", "SP500", "DOW JONES", "NASDAQ", "VIX"]
indice = indice.interpolate(limit_direction='both')

#Calculamos variaciones de cada indice
indice['Variacion MERVAL'] = indice['MERVAL'].pct_change()*100
indice['Variacion BOVESPA'] = indice['BOVESPA'].pct_change()*100
indice['Variacion SP500'] = indice['SP500'].pct_change()*100
indice['Variacion DOW JONES'] = indice['DOW JONES'].pct_change()*100
indice['Variacion NASDAQ'] = indice['NASDAQ'].pct_change()*100
indice['Variacion VIX'] = indice['VIX'].pct_change()*100

#Extraemos columnas variaciones
variaciones = indice[['Variacion MERVAL', 'Variacion BOVESPA', 'Variacion SP500', 'Variacion DOW JONES', 'Variacion NASDAQ', 'Variacion VIX']].copy()
variaciones = variaciones.sort_values('Date', ascending=True)
variaciones.columns = ['MERVAL', 'BOVESPA', 'SP500', 'DOW JONES', 'NASDAQ', 'VIX']
variaciones.dropna()
#Filtramos del 2010 al 2018
indice2 = variaciones.loc['2010-01-01':'2018-01-01']
indice2.dropna()
#Filtramos 2018 adelante (mayor volatilidad)
indice3 = variaciones.loc['2020-02-20':'2020-04-01']
indice3.dropna()

#Heatmap
correlacion = indice3.corr(method='pearson')
correlacion.reset_index()
mask = np.zeros_like(correlacion)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(16, 10))
    mapacalor = sns.heatmap(correlacion, mask=mask, square=True, annot=True, linewidths=.2)
    plt.text(2.25,-.5, "Mapa Calor Indices (COVID)", fontsize = 20, color='Black', fontstyle='italic')
    sns.set(font_scale=2)
    
#Gridplot scatters    
def migridplot(x, y, **kws):
    r = round(x.corr(y), 2)
    r2 = round(x.corr(y)**2, 2)
    ax = plt.gca()
    label = "R = {:.2f} ".format(r) + "\nR2: " + str(r2) 
    ax.annotate(label, xy=(.1, .9), xycoords=ax.transAxes, fontsize = 12, fontweight='bold')
  
sns.set(style="ticks", color_codes=True)
grafico = sns.PairGrid(indice3, corner=True)
grafico.map_diag(sns.distplot, kde=True, color='indianred')
grafico.map_lower(sns.regplot, marker='.', scatter_kws = {'color': 'firebrick', 'alpha':0.4}, line_kws = {'color':'black', 'alpha': 0.7, 'lw':2})
grafico.map_lower(migridplot)
grafico.fig.suptitle("Correlacion Variacion Indices (COVID)", fontsize = 32, color='Black', fontstyle='italic')
grafico.fig.subplots_adjust(wspace=0.2, hspace=0.2)
plt.show()



    

