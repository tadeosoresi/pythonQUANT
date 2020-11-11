# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 18:21:17 2020

@author: tadeo
"""
from pandas_datareader import data as wb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

portafolio = [{'ticker':'AMZN', 'nombre':'Amazon Inc.'}, 
            {'ticker':'NVDA', 'nombre':'NVIDIA'},
            {'ticker':'YPF', 'nombre':'YPF'},
            {'ticker':'INTC', 'nombre':'INTEL'},
            {'ticker':'TSLA', 'nombre':'TESLA'},
            {'ticker':'PBR', 'nombre':'Petroleo Brasileiro'},
            {'ticker':'ETHUSD=X', 'nombre':'Ethereum/USD'}]

portafolio2 = [{'ticker':'AAPL', 'nombre':'APPLE'}, 
            {'ticker':'GGAL', 'nombre':'Grupo financiero Galicia'},
            {'ticker':'AMD', 'nombre':'AMD'},
            {'ticker':'WFC', 'nombre':'Wells Fargo'},
            {'ticker':'MSFT', 'nombre':'Microsoft'},
            {'ticker':'BBD', 'nombre':'Banco Bradesco'},
            {'ticker':'ETHUSD=X', 'nombre':'Ethereum/USD'}]

portafolio3 = [{'ticker':'AAPL', 'nombre':'APPLE'}, 
            {'ticker':'GGAL', 'nombre':'Grupo financiero Galicia'},
            {'ticker':'AMD', 'nombre':'AMD'},
            {'ticker':'WFC', 'nombre':'Wells Fargo'},
            {'ticker':'MSFT', 'nombre':'Microsoft'},
            {'ticker':'BBD', 'nombre':'Banco Bradesco'},
            {'ticker':'ETHUSD=X', 'nombre':'Ethereum/USD'},
            {'ticker':'PAM', 'nombre':'Pampa ADR'}]
#Trata de hacer que la funcion reciba un dict general

def fronteraeficiente(cartera):
    
    datos = pd.DataFrame()
   
    for a in cartera:
        datos[a['ticker']] = wb.DataReader(a['ticker'], data_source='yahoo', 
                                       start='2015-01-01')['Adj Close']
    
        
    global pearson1, pearson2, spearman, kendall, kurtosis, sesgo
    
    #Estadisticas a los distintos activos p/obtener info general
    pearson = datos.corr(method='pearson').round(3)
    spearman = datos.corr(method='spearman').round(3)
    kendall = datos.corr(method='kendall').round(3)
    kurtosis = datos.kurtosis()
    sesgo = datos.skew()
    
    #Porcentaje variacion entre filas, promedio simple retornos & covarianza (mejor std)
    retornos = datos.pct_change().dropna()
    mediaretornos = retornos.mean()*252
    covarianza = retornos.cov()*252

    #Seteamos listas vacias
    retornos_portafolio, volatilidad_portafolio, pf_ratiosharpe, pf_porcentajecomp = ([] for i in range(4))
    #Numero de portafolios basados en distintas combinaciones, no en inversiones!!
    num_portafolios = 8000

    for p in range(num_portafolios):
        pesocomp = np.random.random(int(len(datos.columns)))
        pesocomp /= np.sum(pesocomp)
        retornos2 = np.dot(pesocomp, mediaretornos)
        volatilidad = np.sqrt(np.dot(pesocomp.T, np.dot(covarianza, pesocomp)))
        sharpe = retornos2 / volatilidad
        pf_porcentajecomp.append(pesocomp)
        retornos_portafolio.append(retornos2)
        volatilidad_portafolio.append(volatilidad)
        pf_ratiosharpe.append(sharpe)
        
    
    plt.figure(figsize=(16, 10))
    sns.set(style='darkgrid')
    plt.scatter(x=volatilidad_portafolio, y=retornos_portafolio, c=pf_ratiosharpe, cmap='RdPu')
    plt.colorbar(label='Ratio Sharpe')
    plt.title('Frontera Eficiente Portafolio ', fontsize = 26, fontstyle='italic')
    plt.xlabel('Volatilidad', fontsize = 18)
    plt.ylabel('Retornos', fontsize = 18)
    plt.show()
    
    global portafolio_minvolatilidad, portafolio_maxretorno
    maximo = max(pf_ratiosharpe)
    maximo2 = pf_ratiosharpe.index(maximo)
    comp_vol = pf_porcentajecomp[volatilidad_portafolio.index(min(volatilidad_portafolio))]
    comp_ret = pf_porcentajecomp[retornos_portafolio.index(max(retornos_portafolio))]
    
    portafolio_minvolatilidad = pd.DataFrame(np.round(comp_vol, 3), index=datos.columns, columns=['Composición'])
    portafolio_maxretorno = pd.DataFrame(np.round(comp_ret, 3), index=datos.columns, columns=['Composición'])
    

    datosnorm = datos/datos.iloc[0]
    datosnorm.plot(figsize=(16, 10))
    
fronteraeficiente(portafolio3)