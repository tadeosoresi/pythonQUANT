# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 00:56:57 2020

@author: adria
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as wb
from scipy.stats import norm

#Funcion para obtener datos y generar grafico
def montecarlo(tickeryahoo, nombre):
    data = pd.DataFrame()
    data[tickeryahoo] = wb.DataReader(tickeryahoo, data_source='yahoo', start='2018-01-01')['Adj Close']
    
    #Importamos ultima cotizacion
    import pandas_datareader as pdr
    data2 = pdr.get_data_yahoo('ALUA.BA')
    lastCoti = data2.loc[data2.index[-1], "Adj Close"]
    
    #Mu varianza deriva desviación
    log_returns = np.log(1+ data.pct_change())
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()
    
    #Proyeccion tiempo y simulaciones
    tiempo = 120
    iteraciones = 100
    
    #Escenarios posibles beneficios fut
    daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(tiempo, iteraciones)))
    
    #Dato diario
    di = data.iloc[-1]
    price_list = np.zeros_like(daily_returns)
    price_list[0] = di
    
    for t in range(1, tiempo):
        price_list[t] = price_list[t - 1] * daily_returns[t]
    
   #Grafico
    plt.figure(figsize=(14, 5))
    plt.title("MonteCarlo proyectado a " + nombre)
    plt.ylabel("Precio")
    plt.xlabel("Tiempo")
    plt.plot(price_list)
    plt.axhline(y=lastCoti, xmin=0, xmax=tiempo, color='red', linewidth=2.4, linestyle='--')
    plt.style.use('dark_background')
    log_returns.plot(figsize = (13.5, 4), title=("Retornos logaritmicos"))
    plt.show()

montecarlo('ALUA.BA', 'Aluar Aluminio')
montecarlo('VALO.BA', 'Grupo financiero Valores')


    
        
