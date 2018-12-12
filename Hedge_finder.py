import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import copy
from matplotlib import style
import csv
import time

plt.style.use('ggplot')

start = dt.datetime(2018, 01, 01)
end = dt.datetime(2018, 12, 11)

Ticker_1 = 'INTC'
period = 10
Ticker_2 = ['a']*507
df_1 = web.DataReader(Ticker_1, 'yahoo', start, end)
corr = copy.copy(df_1['Adj Close'])
# ~ corr = np.zeros((len(df_1['Adj Close'])))
t = 0

with open('s&p500_list.csv') as my_file:
	csv_reader = csv.reader(my_file, delimiter = ',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			Ticker_2[t] = row[0]
			t = t + 1
			
highest_relation = np.zeros((len(df_1['Adj Close'])))
lowest_relation = copy.copy(df_1['Adj Close'])

for i in range(0,period):
	corr[i] = 0

t = 0
for t in range(1,500):	
	df_2 = web.DataReader(Ticker_2[t], 'yahoo', start, end)
	print t, Ticker_2[t]
	if len(df_2) != len(df_1) or Ticker_2[t] == Ticker_1:
		df_2 = web.DataReader(Ticker_2[1], 'yahoo', start, end)
	i = 0
	for i in range(period,len(df_1['Adj Close'])):
		corr[i] = np.corrcoef(df_1['Adj Close'][i-period:i],df_2['Adj Close'][i-period:i])[0,1]
	if np.mean(corr[-22:]) == np.mean(highest_relation[-22:]) or np.mean(corr[-22:]) == np.mean(lowest_relation[-22:]):
		print 'uhoh'
	if np.mean(corr[-22:]) > np.mean(highest_relation[-22:]):
		highest_relation = copy.copy(corr)
		most_ticker = Ticker_2[t]
		print 'hello ***** New High'
	if np.mean(corr[-22:]) < np.mean(lowest_relation[-22:]):
		lowest_relation = copy.copy(corr)
		least_ticker = Ticker_2[t]
		print 'hello ***** New Low'

print '*****Most', most_ticker,'*****Least' ,least_ticker
df_2 = web.DataReader(most_ticker, 'yahoo', start, end)
df_3 = web.DataReader(least_ticker, 'yahoo', start, end)

ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 1, colspan = 1, sharex = ax1)

ax1.xaxis_date()

ax1.title.set_text('Correlation Relationship')
ax1.set_xlabel('date')
ax1.set_ylabel('price ($)')
ax1.plot(df_1.index, df_1['Adj Close'], label = Ticker_1)
ax1.plot(df_2.index, df_2['Adj Close'], label = most_ticker)
ax2.bar(df_1.index, highest_relation, label = 'Positive Correlation')
ax1.legend()
ax2.legend()
plt.show()


ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 1, colspan = 1, sharex = ax1)

ax1.xaxis_date()

ax1.title.set_text('Correlation Relationship')
ax1.set_xlabel('date')
ax1.set_ylabel('price ($)')
ax1.plot(df_1.index, df_1['Adj Close'], label = Ticker_1)
ax1.plot(df_3.index, df_3['Adj Close'], label = least_ticker)
ax2.bar(df_1.index, lowest_relation, label = 'Negative Correlation')
ax1.legend()
ax2.legend()
plt.show()
