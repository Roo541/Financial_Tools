import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import math

bank_account= 10000
stocks = 0
amount = 0

style.use('ggplot')

start = dt.datetime(2018,01,01)
end = dt.datetime(2018,10,23)
ticker = 'FB'

df = web.DataReader(ticker, 'yahoo', start, end)

print len(df)

df['9MA'] = df['Adj Close'].rolling(window = 9, min_periods = 0).mean() 
df['50MA'] = df['Adj Close'].rolling(window = 50, min_periods = 0).mean()

		
def Agent_1(bank_account,df,t):
	if df['9MA'][t-1] < df['50MA'][t-1] and df['9MA'][t] > df['50MA'][t] and bank_account > df['Adj Close'][t]:
		choice = 'Buy'
		amount = math.floor(bank_account/(df['Adj Close'][t]))
		return choice, amount
	if df['9MA'][t-1] > df['50MA'][t-1] and df['9MA'][t] < df['50MA'][t]: 
		choice = 'Sell'
		amount = stocks
		return choice, amount
	else:
		return 'none', 0

def Market(bank_account,stocks):
	t = 0
	net = np.zeros((len(df['Adj Close'])))
	net[t] = bank_account + stocks*df['Adj Close'][t]
	for t in range(len(df['Adj Close'])):
		choice,amount = Agent_1(bank_account, df, t)
		if choice == 'Buy':
			stocks = stocks + amount
			bank_account = bank_account - amount*float(df['Adj Close'][t])
			net[t] = bank_account + stocks*df['Adj Close'][t]
		if choice == 'Sell':
			stocks = stocks - amount
			bank_account = bank_account + amount*float(df['Adj Close'][t])	
			net[t] = bank_account + stocks*df['Adj Close'][t]
		else:
			net[t] = bank_account + stocks*df['Adj Close'][t]
	return bank_account, stocks, net,t
		
a, b, c,t  = Market(bank_account, stocks)

print 'Bank Account %d' %a,'\n', 'Stocks of', ticker, 'held %d' %b, '\n', 'Net worth %d' %c[t]

g = np.arange(0, len(c), 1)

plt.figure()
plt.plot(g, c, label = 'Net Worth')
plt.legend()

plt.figure()
ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5 , colspan = 1 )
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 5, colspan = 1, sharex = ax1)


ax1.plot(df.index, df['Adj Close'], label = 'price')
ax1.plot(df.index, df['9MA'], label = '9MA')
ax1.plot(df.index, df['50MA'], label = '50MA')
ax2.bar(df.index, df['Volume'], label = 'Volume')
ax1.legend()
ax2.legend()
plt.show()
