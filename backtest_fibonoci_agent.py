import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import math


initial = 10000
bank_account= initial
stocks = 0
shares = 0

#Agent 3
Low = 1000
High = 1

style.use('ggplot')

start = dt.datetime(2017,01,01)
end = dt.datetime(2018,11,04)
ticker = 'QQQ'

df = web.DataReader(ticker, 'yahoo', start, end)

df['9MA'] = df['Adj Close'].rolling(window = 9, min_periods = 0).mean() 
df['50MA'] = df['Adj Close'].rolling(window = 50, min_periods = 0).mean()
		
def Agent_1(bank_account, stocks, df, t):
	if df['9MA'][t-1] < df['50MA'][t-1] and df['9MA'][t] > df['50MA'][t] and bank_account > df['Adj Close'][t]:
		choice = 'Buy'
		shares = math.floor(bank_account/(df['Adj Close'][t]))
		return choice, shares
	if df['9MA'][t-1] > df['50MA'][t-1] and df['9MA'][t] < df['50MA'][t]: 
		choice = 'Sell'
		shares = stocks
		return choice, shares
	else:
		return 'none', 0

#Trading from derivative		
def Agent_2(bank_account, stocks, df, t):
	dt=.01
	if (df['9MA'][t-1]-df['9MA'][t-2])/dt < 0 and (df['9MA'][t]-df['9MA'][t-1])/dt > 0 and bank_account > df['Adj Close'][t]:
		choice = 'Buy'
		shares = math.floor(bank_account/(df['Adj Close'][t]))
		return choice, shares
	if (df['9MA'][t-1]-df['9MA'][t-2])/dt > 0 and (df['9MA'][t]-df['9MA'][t-1])/dt < 0: 
		choice = 'Sell'
		shares = stocks
		return choice, shares
	else:
		return 'none', 0
		
#fibonoci agent
def Agent_3(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last):
	period = 10
	for t in range(t-period,t):
		if df['Adj Close'][t-period] <= Low:
			Low = df['Adj Close'][t-period]
			low_dummy = t-period
		if df['Adj Close'][t-period] >= High:
			High = df['Adj Close'][t-period]
			high_dummy = t-period
	buy_target = High-.618*(High-Low)
	sell_target = High + 1.618*(High-Low)
	#stop loss
	if df['Adj Close'][t] <= (buy_price - .05*buy_price) and stocks > 0:
		choice = 'Sell'
		shares = stocks
		return choice, shares
	if df['Adj Close'][t] >= df['Adj Close'][high_dummy]:
		choice = 'Sell'
		shares = math.ceil(stocks/2)
		return choice, shares
	if df['Adj Close'][t] >= buy_target-.01*buy_target and df['Adj Close'][t] <= buy_target+.01*buy_target and bank_account >= df['Adj Close'][t]:
		choice = 'Buy'
		shares = math.floor(bank_account/df['Adj Close'][t])
		return choice, shares
	if df['Adj Close'][t] >= sell_target-.01*sell_target and df['Adj Close'][t] <= sell_target+.01*sell_target and stocks > 0:
		choice = 'Sell'
		shares = stocks
		return choice, shares
	else:
		return 'none', 0
#better fibonoci agent		
def Agent_4(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last, high_dummy):
	period = 20
	if last == 'Sell' or last == 'none':
		Low = 1000
		High = 1
		for t in range(t-period,t):
			if df['Adj Close'][t-period] <= Low:
				Low = df['Adj Close'][t-period]
				low_dummy = t-period
			if df['Adj Close'][t-period] >= High:
				High = df['Adj Close'][t-period]
				high_dummy = t-period
		buy_target = High-.618*(High-Low)
		sell_target = High + .618*(High-Low)
		if df['Adj Close'][t] >= buy_target-.015*buy_target and df['Adj Close'][t] <= buy_target+.015*buy_target and bank_account >= df['Adj Close'][t]:
			choice = 'Buy'
			shares = math.floor(int(bank_account)/float(df['Adj Close'][t]))
			return choice, shares, high_dummy, High, Low
		return 'none', 0, high_dummy, High, Low
	
	if last == 'Buy':
		sell_target = High + .618*(High-Low)
		#stop loss
		if df['Adj Close'][t] <= (buy_price - .05*buy_price) and stocks > 0:
			choice = 'Sell'
			shares = stocks
			return choice, shares, high_dummy, High, Low
		if df['Adj Close'][t] >= df['Adj Close'][high_dummy]:
			choice = 'Sell'
			shares = math.ceil(stocks/2)
			return choice, shares, high_dummy, High, Low
		if df['Adj Close'][t] >= sell_target-.015*sell_target and df['Adj Close'][t] <= sell_target+.015*sell_target and stocks > 0:
			choice = 'Sell'
			shares = stocks
			return choice, shares, high_dummy, High, Low
		else:
			return 'none', 0, high_dummy, High, Low
	
def Market(bank_account, stocks, df, Low, High):
	t = 0
	buy_price = 1
	sell_price = 1
	last = 'none'
	high_dummy = 0
	net = np.zeros((len(df['Adj Close'])))
	net[t] = bank_account + stocks*df['Adj Close'][t]
	for t in range(len(df['Adj Close'])):
		# ~ print 'it is now round %d' %t
		#choice, shares = Agent_1(bank_account, stocks, df, t)
		choice, shares, high_dummy, high, low = Agent_4(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last, high_dummy)
		if choice == 'Buy' and bank_account >= shares*df['Adj Close'][t]:
			#print 'Bank Account %d' %bank_account, 'Number of Shares %d'  %shares
			stocks = stocks + shares
			bank_account = bank_account - shares*df['Adj Close'][t]
			net[t] = bank_account + stocks*df['Adj Close'][t]
			buy_price = df['Adj Close'][t]
			last = 'Buy'
			high_dummy = high_dummy
			High = high
			Low = low
			# ~ print 'Buy price is $%d' %df['Adj Close'][t], 'Bank account value is $%d' %bank_account, 'Number of shares %d' %shares
		if choice == 'Sell' and shares > 0:	
			#print 'Bank Account %d' %bank_account, 'Number of Shares%d'  %shares
			bank_account = bank_account + shares*df['Adj Close'][t]
			stocks = stocks - shares
			net[t] = bank_account + stocks*df['Adj Close'][t]
			sell_price = df['Adj Close'][t]
			last = 'Sell'
			# ~ print 'Sell price is $%d' %df['Adj Close'][t], 'Bank account value is $%d' %bank_account, 'Number of shares %d' %shares
		else:
			net[t] = bank_account + stocks*df['Adj Close'][t]
	return bank_account, stocks, net, t
		
bank_account, stocks, net, t  = Market(bank_account, stocks, df, Low, High)

r = float((net[t]/initial -1))*100

print 'Bank Account %d' %bank_account,'\n', 'Stocks of', ticker, 'held %d' %stocks, '\n', 'Net worth $%d' %net[t], '\n', 'Return Percentage %f' %r

plt.figure()
plt.plot(df.index, net, label = 'Net Worth')
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
