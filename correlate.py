import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import copy
from matplotlib import style

plt.style.use('ggplot')

start = dt.datetime(2015, 01, 01)
end = dt.datetime(2018, 11, 02)

Ticker_1 = 'INTC'
Ticker_2 = 'AMD'
period = 20

df_1 = web.DataReader(Ticker_1, 'yahoo', start, end)
df_2 = web.DataReader(Ticker_2, 'yahoo', start, end)

#corr = np.zeros((len(df_1['Adj Close'])))
corr = copy.copy(df_1['Adj Close'])

for i in range(period):
	corr[i] = 0


for i in range(period,len(df_1['Adj Close'])):
	corr[i] = np.corrcoef(df_1['Adj Close'][i-period:i],df_2['Adj Close'][i-period:i])[0,1]

ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 1, colspan = 1, sharex = ax1)
ax1.xaxis_date()

print df_1['Adj Close'].tail()

ax1.title.set_text('Correlation Relationship')
ax1.set_xlabel('date')
ax1.set_ylabel('price ($)')
ax1.plot(df_1.index, df_1['Adj Close'], label = Ticker_1)
ax1.plot(df_2.index, df_2['Adj Close'], label = Ticker_2)
ax2.bar(corr.index, corr, label = 'Correlation')
ax1.legend()
ax2.legend()
plt.show()
