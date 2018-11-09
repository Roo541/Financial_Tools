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
end = dt.datetime(2018,11,07)
ticker = 'SPY'

df = web.DataReader(ticker, 'yahoo', start, end)

df['9MA'] = df['Adj Close'].rolling(window = 9, min_periods = 0).mean() 
df['200MA'] = df['Adj Close'].rolling(window = 200, min_periods = 0).mean()

r = np.zeros((len(df['Adj Close'])))

transactions = [(0,0,0,0)]*len(df['Adj Close'])
		
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

def agent_7(bank_account, stocks, df, t, Low, High, buy_price, sell_price, buy_target, sell_target, x, last):
	period = 10
	if df['Adj Close'][t] <= (buy_price - .01*buy_price) or df['Adj Close'][t] < (df['Adj Close'][t-1]-.0075*df['Adj Close'][t-1]):
		choice = 'Sell'
		shares = stocks
		return choice, shares, High, Low, buy_target, sell_target, x, last	
	L = df['Adj Close'].rolling(window = period, min_periods = 0).min()
	H = df['Adj Close'].rolling(window = period, min_periods = 0).max()
	Low = L[t]
	High = H[t]
	difference = High - Low
	twenty = High - .236*difference
	thirty = High - .382*difference
	fifty = High - .5*difference
	sixty = High - .618*difference
	if df['Adj Close'][t] <= twenty:
		x = 'thirty'
		buy_target = Low + .78*difference
		return 'none', 0, High, Low, buy_target, sell_target, x, last
	if df['Adj Close'][t] <= thirty:
		x = 'thirty'
		buy_target = Low + .64*difference
		return 'none', 0, High, Low, buy_target, sell_target, x, last
	if df['Adj Close'][t] <= fifty:
		x = 'fifty'
		buy_target = Low + .52*difference
		return 'none', 0, High, Low, buy_target, sell_target, x, last
	if df['Adj Close'][t] <= sixty :
		x = 'sixty'
		buy_target = Low + .40*difference
		return 'none', 0, High, Low, buy_target, sell_target, x, last
	if df['Adj Close'][t] >= buy_target and bank_account > 0 and last == 'none' or last == 'Sell':
		if df['Adj Close'][t] > df['200MA'][t]:
			choice = 'Buy'
			shares = int(bank_account/df['Adj Close'][t])-1
			sell_target = High + .618*difference
			return choice, shares, High, Low, buy_target, sell_target, x, last
		return 'none', 0, High, Low, buy_target, sell_target, x, last
	if df['Adj Close'][t] >= sell_target and stocks > 0:
		choice = 'Sell'
		shares = stocks
		return choice, shares, High, Low, buy_target, sell_target, x, last
	return 'none', 0, High, Low, buy_target, sell_target, x, last

def percent_return(net,t, initital):
	r[t] = float((net[t]/initial -1))*100
	return r		
	
def Market(bank_account, stocks, df, Low, High, transactions):
	t = 0
	df['200MA'] = df['Adj Close'].rolling(window = 200, min_periods = 0).mean()
	trigger = 'none'
	buy_target = 0
	sell_target = 0
	x = 'none'
	buy_price = 1
	sell_price = 1
	last = 'none'
	high_dummy = 0
	low_dummy = 1000
	net = np.zeros((len(df['Adj Close'])))
	net[t] = bank_account + stocks*df['Adj Close'][t]
	for t in range(len(df['Adj Close'])):
		# ~ print 'it is now round %d' %t
		#choice, shares = Agent_2(bank_account, stocks, df, t)
		#choice, shares = Agent_3(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last)
		#choice, shares, high_dummy, high, low,low_dummy, trigger, buy_target = Agent_5(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last, high_dummy, low_dummy, trigger, buy_target)
		#choice, shares, high_dummy, high, low,low_dummy, trigger, buy_target =Agent_5(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last, high_dummy, low_dummy,trigger, buy_target)
		#choice, shares, high, low, trigger, buy_target =Agent_6(bank_account, stocks, df, t, Low, High, buy_price, sell_price, last, trigger, buy_target)
		choice, shares, high, low, buy_target, sell_target, x, last = agent_7(bank_account, stocks, df, t, Low, High, buy_price, sell_price, buy_target, sell_target, x, last)
		if choice == 'Buy' and bank_account >= shares*df['Adj Close'][t]:
			stocks = stocks + shares
			bank_account = bank_account - shares*df['Adj Close'][t]
			net[t] = bank_account + stocks*df['Adj Close'][t]
			buy_price = df['Adj Close'][t]
			last = 'Buy'
			high_dummy = high_dummy
			High = high
			buy_target = 0 
			Low = low
			percent_return(net, t, initial)
			sell_target =  sell_target
			for i in range(len(df['Adj Close'])):
				if transactions[i] == (0,0,0,0):
					transactions[i] = ('Buy', df['Adj Close'][t], df.index[t], shares)
					break	
			# ~ print 'Bought %d shares at ' %shares ,df.index[t], stocks, df['Adj Close'][t]
			#print 'Buy price is $%d' %df['Adj Close'][t], 'Bank account value is $%d' %bank_account, 'Number of shares %d' %shares
		if choice == 'Sell' and shares > 0:	
			#print 'Bank Account %d' %bank_account, 'Number of Shares%d'  %shares
			bank_account = bank_account + shares*df['Adj Close'][t]
			stocks = stocks - shares
			net[t] = bank_account + stocks*df['Adj Close'][t]
			sell_price = df['Adj Close'][t]
			last = 'Sell'
			low_dummy = 1000
			high_dummy = 1
			High = high
			Low = low
			buy_target = 0
			percent_return(net, t, initial)
			if stocks > 0:
				last = 'none'
			for i in range(len(df['Adj Close'])):
				if transactions[i] == (0,0,0,0):
					transactions[i] = ('Sold', df['Adj Close'][t], df.index[t], shares)
					break	
			#print 'Sold %d shares at ' %shares, df.index[t], stocks, df['Adj Close'][t]
			#print 'Sell price is $%d' %df['Adj Close'][t], 'Bank account value is $%d' %bank_account, 'Number of shares %d' %shares
		else:
			net[t] = bank_account + stocks*df['Adj Close'][t]
			percent_return(net, t, initial)
	return bank_account, stocks, net, t
		
bank_account, stocks, net, t  = Market(bank_account, stocks, df, Low, High, transactions)

a = float((net[t]/initial -1))*100

r = percent_return(net, t, initial)
for i in range(len(df)):
	if transactions[i] != (0,0,0,0):
		print transactions[i]
print 'Bank Account %d' %bank_account,'\n', 'Stocks of', ticker, 'held %d' %stocks, '\n', 'Net worth $%d' %net[t], '\n', 'Return Percentage %f' %a

plt.figure()
plt.plot(df.index, net, label = 'Net Worth')
plt.legend()

plt.figure()
ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5 , colspan = 1 )
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 5, colspan = 1, sharex = ax1)

plt.figure()
plt.plot(df.index, r, label = 'Percent Return')
plt.legend()

ax1.plot(df.index, df['Adj Close'], label = 'price')
ax1.plot(df.index, df['9MA'], label = '9MA')
ax1.plot(df.index, df['200MA'], label = '200MA')
ax2.bar(df.index, df['Volume'], label = 'Volume')
ax1.legend()
ax2.legend()
plt.show()
