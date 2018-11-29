import datetime as dt
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
import csv

style.use('ggplot')

start = dt.datetime(2018,01,01)
end = dt.datetime(2018,11,28)

# ~ ticker = 'INTC'

# ~ df = web.DataReader(ticker, 'yahoo', start, end)

# ~ df['50_MA'] = df['Adj Close'].rolling(window = 50, min_periods = 0).mean()

# Searching for buying opportunities
ticker = ['a']*507
t = 0
order = True
with open('s&p500_list.csv') as my_file:
	csv_reader = csv.reader(my_file, delimiter = ',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			ticker[t] = row[0]
			t = t + 1
choice = ''
stock = ['none']*len(ticker)
t = 21
Bank_Account = 100000.0
High = 0.0
Low = 0.0
buy_target = 0.0
sell_target = 10000.0
shares = 0
difference = 0.0
buy_price = 0.0
for i in range(1,500):
	print i, ticker[i]
	dt = web.DataReader(ticker[i], 'yahoo', start, end)
	dt['50_MA'] = dt['Adj Close'].rolling(window = 50, min_periods = 0).mean()
	date_high = dt.index[0]
	date_low = dt.index[1]
	period = 20
	order = True
	print 'this is a check', Bank_Account
	print shares
	print stock
	while order == True:
		current = dt['Adj Close'][t]
		if current < (buy_price - buy_price*.02) or current < (dt['Adj Close'][t-1] - .02*dt['Adj Close'][t-1]):
			Bank_Account = Bank_Account + shares*dt['Adj Close'][t]
			sell_target = 10000.0
			buy_target = 0.0
			buy_price = 0.0
			shares = 0
			print 'stop lossed at', dt['Adj Close'][t]
			print 'Bank account at', Bank_Account		
		if current > High:
			High = current
			date_high = dt.index[t]
		if current < Low:
			Low = current
			date_low = dt.index[t]
		if date_high < dt.index[t-period]:
			High = 0.0
			date_high = dt.index[0]
		if date_low < dt.index[t-period]:
			Low = 10000.0
			date_low = dt.index[1]
		if Low != 10000.0 and High != 0.0 and Low < High:
			difference = High - Low
			twenty = High - .236*difference
			thirty = High - .382*difference
			fifty = High - .5*difference
			sixty = High - .618*difference
		if current < twenty and difference != 0:
			buy_target = twenty + .0025*twenty
		if current < thirty and difference != 0:
			buy_target = thirty + .0025*thirty
		if current < fifty and difference != 0:
			buy_target = fifty + .0025*fifty
		if current < sixty and difference != 0:
			buy_target = sixty + .0025*sixty
		if current >= buy_target and buy_target != 0 and shares == 0:
			stock = ticker[i]
			shares = int((.10*Bank_Account)/(dt['Adj Close'][t]))
			Bank_Account = Bank_Account - shares*dt['Adj Close'][t]
			sell_target = High + 1.618*difference	
			buy_target = 0.0
			buy_price = dt['Adj Close'][t]
			print 'bought shares', shares
			print 'Bank account at', Bank_Account
		if current >= sell_target:
			Bank_Account = Bank_Account + shares*dt['Adj Close'][t]
			sell_target = 10000.0
			buy_target = 0.0
			buy_price = 0.0
			shares = 0
			print 'sold shares', shares
			print 'Bank account at', Bank_Account		
		Net_worth = Bank_Account + shares*dt['Adj Close'][t]
				
		t = t + 1
		if t >= len(dt):
			order = False
			Bank_Account = Bank_Account + shares*dt['Adj Close'][t-1]
			sell_target = 10000.0
			buy_target = 0.0
			buy_price = 0.0
			shares = 0
			print 'Net worth is ', Net_worth
			print 'Bank Account valued at ', Bank_Account
			print 'Number of shares ', shares
			print 'Current Stock price ', dt['Adj Close'][t-1]
			t = 0
			time.sleep(1)


	








# cleaning up the tickers that qualified
# ~ count = 0
# ~ for i in range(len(stock)):
	# ~ if stock[i] != 'none':
		# ~ count = count + 1
# ~ print count
# ~ watch = ['']*count
# ~ dummy = 0
# ~ for i in range(len(stock)):
	# ~ if stock[i] != 'none' and dummy <= count:
		# ~ watch[dummy] = stock[i]
		# ~ dummy = dummy + 1

# ~ print len(watch)
# ~ print watch



# ~ for t in range(0,len(dt)):
		# ~ if dt['Adj Close'][t] < dt['50_MA'][t]:
			# ~ choice = 'Below MA'
			# ~ stock[i] = ticker[i]

























# ~ plt.plot(df.index, df['50_MA'])




