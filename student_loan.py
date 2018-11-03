import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime as dt 
import numpy as np
from matplotlib import style

interest = 4.29/12
t = 12
total = 1854
initial = 1854
month = ['Jan', 'Feb', 'Mar', 'April', 'Jun', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan']
for i in range(len(month)):
		total = total + initial*(interest/100)
		initial = total
		print month[i], total
