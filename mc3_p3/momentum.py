import datetime as dt
from util import get_data, plot_data
import math
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def cal_momentum(N = 10,sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), \
    syms = ['IBM'],gen_plot=False):
	#READ IN DATA
	dates = pd.date_range(sd, ed)
	prices_all = get_data(syms, dates)  
	prices = prices_all[syms]  
	prices_IBM = prices_all['IBM']
	rs = []
	for i in range(0,len(prices_IBM[N:])):
	     row=[]
	     time=prices_IBM.index[i+N]
	     row.append(time)
	     row.append(prices_IBM[i+N])
	     day_N=prices_IBM[i]
	     row.append(day_N)
	     mom=(prices_IBM[i+N]-day_N)/day_N
	     row.append(mom)
	     rs.append(row)
	colname=['Date','Price','Price-Before-N-Days','Momentum']
	rs = pd.DataFrame(rs[0:],columns=colname)
	#print rs

	if gen_plot:
		rs.plot(x='Date',y='Momentum',fontsize=14)
		plt.show()
	return rs


if __name__ == "__main__":
	cal_momentum(gen_plot=True)