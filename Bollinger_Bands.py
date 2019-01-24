import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import copy
from matplotlib import style
import csv
import time
import math


start = dt.datetime(2018, 01, 01)
end = dt.datetime(2019, 01, 23)
ticker = 'ROKU'

df = web.DataReader(ticker, 'yahoo', start, end)

std = [np.nan]*len(df)

df['20MA'] = df['Adj Close'].rolling(window = 20, min_periods = 0).mean()

df['20Std'] = df['Adj Close'].rolling(window = 20, min_periods = 0).std()

df['UpperBand'] = df['20MA']
df['LowerBand'] = df['20MA']

for i in range(0,len(df)):
	df['UpperBand'][i] = df['20MA'][i] + df['20Std'][i]*2
	df['LowerBand'][i] = df['20MA'][i] - df['20Std'][i]*2

plt.plot(df.index, df['Adj Close'], 'k', label = ticker) 	
plt.plot(df.index, df['20MA'], 'r', label = '20MA')
plt.plot(df.index, df['UpperBand'], 'b', label = 'Upper Band')
plt.plot(df.index, df['LowerBand'], 'b', label = 'Lower Band')

initial = 10000.0
bankAccount = initial
shares = 0
buy_price = 0
price_target = 0
t = 0

while t < len(df):
	current = df['Adj Close'][t]
	upper = df['UpperBand'][t]
	lower = df['LowerBand'][t]
	
	if current <= buy_price - buy_price*.02:
		bankAccount = bankAccount + shares*current
		shares = 0
		print 'Stop Lossed', 'current price $', current
		print df.index[t]
		print bankAccount, shares
		buy_price = 0	
		price_target = 0
	
	if current < lower and buy_price == 0:
		shares = math.floor(bankAccount/current)
		bankAccount = bankAccount - shares*current
		print 'need to buy', 'current price $', current
		print df.index[t]
		print bankAccount, shares
		buy_price = current
		price_target = buy_price + buy_price*.05
	
	if buy_price != 0 and current >= price_target:
		bankAccount = bankAccount + shares*current
		shares = 0
		print 'Selling Shares', 'current price $', current
		print df.index[t]
		print bankAccount, shares
		buy_price = 0	
		price_target = 0
	
	t = t + 1

bankAccount = bankAccount + shares*current
return_val = (bankAccount/initial - 1)*100
print bankAccount
print shares
print '% return ', return_val


plt.legend()
plt.show()


