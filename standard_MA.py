import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np

style.use('ggplot')

start = dt.datetime(2000,01,01)
end = dt.datetime(2018,10,23)
ticker = 'TSLA'

df = web.DataReader(ticker, 'yahoo', start, end)
df1 = web.DataReader('QQQ', 'yahoo', start, end)

df['100MA'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean() 
print df['Close'].corr(df1,method = 'pearson', min_periods = 1)

ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5 , colspan = 1 )
ax2 = plt.subplot2grid((6,1),(5,0), rowspan = 5, colspan = 1, sharex = ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100MA'])
ax2.bar(df.index, df['Volume'])
plt.show()
