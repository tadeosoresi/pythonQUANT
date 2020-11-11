# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 23:25:33 2020

@author: adria
"""


import pandas as pd
import matplotlib.pyplot as plt
import datetime
from pandas_datareader import data as wb

#Datos Merval
merval = wb.DataReader('^MERV', 'yahoo', start='2010-01-01')
merval.rename(columns={'Adj Close':'AdjClose'}, inplace=True)
merval = merval.sort_values('Date', ascending=True)
merval.rename(columns={'Cierre':'AdjClose'}, inplace=True)
merval['Variaciones'] = merval['AdjClose'].pct_change()*100


#Primer filtro año 2014 a 2019
merval2 = merval.loc['2014-09-30':'2019-08-01']
merval2 = merval2[::-1]
#Filtro PASO
mervalPASO = merval.loc['2019-08-09':'2019-10-10']
mervalPASO = mervalPASO[::-1]
#Filtro Coronavirus
mervalCOVID = merval.loc['2020-02-03':'2020-03-27']
mervalCOVID = mervalCOVID[::-1]

#Datos Aluar
alua = wb.DataReader('ALUA.BA', 'yahoo', start='2010-01-01')
alua.rename(columns={'Adj Close':'AdjClose'}, inplace=True)
alua = alua.sort_values('Date', ascending=True)
alua['Variaciones'] = alua['AdjClose'].pct_change()*100

#Primer filtro año 2014 a 2019
alua2 = alua.loc['2014-09-30':'2019-08-01']
alua2 = alua2[::-1]
#Segundo filtro PASO
aluaPASO = alua.loc['2019-08-09':'2019-10-10']
aluaPASO = aluaPASO[::-1]
#Filtro Coronavirus
aluaCOVID = alua.loc['2020-02-03':'2020-03-27']
aluaCOVID = aluaCOVID[::-1]

#Datos TXAR
txar = pd.read_excel('TXAR.xlsx')
txar = txar.sort_values('Fecha', ascending=True)
txar.rename(columns={'Cierre':'AdjClose'}, inplace=True)
txar['Variaciones'] = txar['AdjClose'].pct_change()*100
txar.set_index('Fecha', inplace=True)

#Primer filtro año 2014 a 2019
txar2 = txar.loc['2014-09-30':'2019-08-01']
txar2 = txar2[::-1]
#Filtro PASO
txarPASO = txar.loc['2019-08-09':'2019-10-10']
txarPASO = txarPASO[::-1]
#Filtro Coronavirus
txarCOVID = txar.loc['2020-02-03':'2020-03-27']
txarCOVID = txarCOVID[::-1]

#Datos Tenaris 2014 a 2019
ts = pd.read_excel('TS.xlsx')
ts = ts.sort_values('Fecha', ascending=True)
ts.rename(columns={'Cierre':'AdjClose'}, inplace=True)
ts['Variaciones'] = ts['AdjClose'].pct_change()*100
ts.set_index('Fecha', inplace=True)

#Primer filtro año 2014 a 2019
ts2 = ts.loc['2014-09-30':'2019-08-01']
ts2 = ts2[::-1]
#Filtro PASO
tsPASO = ts.loc['2019-08-09':'2019-10-10']
tsPASO = tsPASO[::-1]
#No hay filtro coronavirus por baja cotizacion

#Escenario1 2014-2019
correlacion = pd.concat([merval2['Variaciones'], alua2['Variaciones'], txar2['Variaciones'], ts2['Variaciones']], axis=1)
correlacion.columns = ['Merval', 'ALUA', 'TXAR', 'TS']
correlacion = correlacion.interpolate(limit_direction='both')

#Escenario PASO
PASO = pd.concat([mervalPASO['Variaciones'], aluaPASO['Variaciones'], txarPASO['Variaciones'], tsPASO['Variaciones']], axis=1)
PASO.columns = ['Merval', 'ALUA', 'TXAR', 'TS']
PASO = PASO.interpolate(limit_direction='both')

#Escenario COVID
COVID = pd.concat([mervalCOVID['Variaciones'], aluaCOVID['Variaciones'], txarCOVID['Variaciones']], axis=1)
COVID.columns = ['Merval', 'ALUA', 'TXAR']
COVID = COVID.interpolate(limit_direction='both')

#Recta regresion y scatter ALUA MERVAL 2014-2019
x4 = correlacion.ALUA
y2 = correlacion.Merval
b1111 = x4.cov(y2) / x4.var()
b0000 = y2.mean() - b1111*x4.mean()
recta4 = b0000 + b1111*x4

fig, ax = plt.subplots(figsize=(20, 7), nrows=1, ncols=3)
ax[0].scatter(x4, y2, marker='.', s=8)
ax[0].plot(x4, recta4, color='red', lw=1)
ax[0].set_xlim((-15, 15))
ax[0].set_ylim((-15, 15))
ax[0].set_xlabel("ALUAR")
ax[0].set_ylabel("Merval")
ax[0].set_title("Correlacion de variaciones Merval y ALUAR 2014-2019")

#Recta regresion y scatter TXAR MERVAL 2014-2019
x5 = correlacion.TXAR
y2 = correlacion.Merval
b11111 = x5.cov(y2) / x5.var()
b00000 = y2.mean() - b11111*x5.mean()
recta5 = b00000 + b11111*x5

ax[1].scatter(x5, y2, marker='.', s=8)
ax[1].plot(x5, recta5, color='red', lw=1)
ax[1].set_xlim((-15, 15))
ax[1].set_ylim((-15, 15))
ax[1].set_xlabel("TERNIUM-SIDERAR")
ax[1].set_ylabel("Merval")
ax[1].set_title("Correlacion de variaciones Merval y TXAR 2014-2019")

#Recta regresion y scatter TS MERVAL 2014-2019
x6 = correlacion.TS
y2 = correlacion.Merval
b111111 = x6.cov(y2) / x6.var()
b000000 = y2.mean() - b111111*x6.mean()
recta6 = b000000 + b111111*x6

ax[2].scatter(x6, y2, marker='.', s=8, color='black')
ax[2].plot(x6, recta6, color='red', lw=1)
ax[2].set_xlim((-15, 15))
ax[2].set_ylim((-15, 15))
ax[2].set_xlabel("TENARIS")
ax[2].set_ylabel("Merval")
ax[2].set_title("Correlacion de variaciones Merval y TS 2014-2019")

fig.subplots_adjust(wspace=0.5)
plt.show()


#Recta regresion y scatter ALUA MERVAL PASO
x2 = PASO.ALUA
y = PASO.Merval
b11 = x2.cov(y) / x2.var()
b00 = y.mean() - b11*x2.mean()
recta2 = b00 + b11*x2


fig, ax = plt.subplots(figsize=(20, 7), nrows=1, ncols=3)

ax[0].scatter(x2, y, marker='o', s=8)
ax[0].plot(x2, recta2, color='red', lw=1)
ax[0].set_xlim((-15, 15))
ax[0].set_ylim((-15, 15))
ax[0].set_xlabel("ALUAR")
ax[0].set_ylabel("Merval")
ax[0].set_title("Correlacion de variaciones Merval y ALUAR PASO")


#Recta regresion y scatter TXAR MERVAL PASO
x3 = PASO.TXAR
y = PASO.Merval
b111 = x3.cov(y) / x3.var()
b000 = y.mean() - b111*x3.mean()
recta3 = b000 + b111*x3


ax[1].scatter(x3, y, marker='o', s=8)
ax[1].plot(x3, recta3, color='red', lw=1)
ax[1].set_xlim((-15, 15))
ax[1].set_ylim((-15, 15))
ax[1].set_xlabel("TERNIUM-SIDERAR")
ax[1].set_ylabel("Merval")
ax[1].set_title("Correlacion de variaciones Merval y TXAR PASO")


#Recta regresion y scatter TS MERVAL PASO
x = PASO.TS
y = PASO.Merval
b1 = x.cov(y) / x.var()
b0 = y.mean() - b1*x.mean()
recta = b0 + b1*x
r = round(x.corr(y), 2)
r2 = round(x.corr(y)**2, 2)

legend = "r2: " +str(r2)+ "\nr: " +str(r)+ "\nb: " + str(round(b1, 2))
ax[2].scatter(x, y, marker='o', s=8, color='black')
ax[2].plot(x, recta, color='red', lw=1, label=legend)
ax[2].set_xlim((-15, 15))
ax[2].set_ylim((-15, 15))
ax[2].set_xlabel("TS")
ax[2].set_ylabel("Merval")
ax[2].set_title("Correlacion de variaciones Merval y TS PASO")
plt.legend()

fig.subplots_adjust(wspace=0.5)
plt.show()

#Recta regresion y scatter ALUA MERVAL COVID
x7 = COVID.ALUA
y3 = COVID.Merval
b1111111 = x7.cov(y3) / x7.var()
b0000000 = y3.mean() - b1111111*x7.mean()
recta7 = b0000000 + b1111111*x7

fig, ax = plt.subplots(figsize=(20, 7), nrows=1, ncols=2)
ax[0].scatter(x7, y3, marker='.', s=25, color='black')
ax[0].plot(x7, recta7, color='red', lw=1)
ax[0].set_xlim((-15, 15))
ax[0].set_ylim((-15, 15))
ax[0].set_xlabel("ALUAR")
ax[0].set_ylabel("Merval")
ax[0].set_title("Correlacion de variaciones Merval y ALUAR COVID")

#Recta regresion y scatter TXAR MERVAL COVID
x8 = COVID.TXAR
y3 = COVID.Merval
b11111111 = x8.cov(y3) / x8.var()
b00000000 = y3.mean() - b11111111*x8.mean()
recta8 = b00000000 + b11111111*x8

ax[1].scatter(x8, COVID.Merval, marker='.', s=25, color='black')
ax[1].plot(x8, recta8, color='red', lw=1)
ax[1].set_xlim((-15, 15))
ax[1].set_ylim((-15, 15))
ax[1].set_xlabel("TERNIUM-SIDERAR")
ax[1].set_ylabel("Merval")
ax[1].set_title("Correlacion de variaciones Merval y TXAR COVID")

fig.subplots_adjust(wspace=0.2)
plt.show()



