import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import datetime as dt
import copy

style.use('ggplot')

start = dt.datetime(2016, 01, 01)
end = dt.datetime(2018, 10, 22)

Ticker = 'AAPL'
#Moving averages
p_0 = 50
p_1 = 100
p_2 = 200
df = web.DataReader(Ticker, 'yahoo', start, end)

SMA_0 = copy.copy(df)
SMA_1 = copy.copy(df)
SMA_2 = copy.copy(df)

for i in range(p_0):
	SMA_0['Close'][i] = 0
for i in range(p_1):
	SMA_1['Close'][i] = 0
for i in range(p_2):
	SMA_2['Close'][i] = 0

for i in range(p_0,len(df)):
		SMA_0['Close'][i] = (np.sum([df['Close'][i-p_0:i]]))/p_0
		
for i in range(p_1,len(df)):
		SMA_1['Close'][i] = (np.sum([df['Close'][i-p_1:i]]))/p_1

for i in range(p_2,len(df)):
		SMA_2['Close'][i] = (np.sum([df['Close'][i-p_2:i]]))/p_2

plt.plot(SMA_0['Close'][p_0:], label = '50 Day MA')
plt.plot(SMA_1['Close'][p_1:], label = '100 Day MA')
plt.plot(SMA_2['Close'][p_2:], label = '200 Day MA')
plt.plot(df['Close'], label = 'price')
plt.title(Ticker)
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.show()












