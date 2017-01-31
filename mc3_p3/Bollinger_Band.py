import datetime as dt
from util import get_data, plot_data
import math
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def cal_bb(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), \
    syms = ['IBM'],gen_plot=False):
	#READ IN DATA
	dates = pd.date_range(sd, ed)
	prices_all = get_data(syms, dates)  
	prices = prices_all[syms]  
	prices_IBM = prices_all['IBM']
	rs = []
	for i in range(0,len(prices_IBM[10:])):
		row=[]
		time=prices_IBM.index[i+10]
		row.append(time)
		row.append(prices_IBM[i+10])
		avg_10=prices_IBM[i:i+10].sum(axis=0)/10
		row.append(avg_10)
		std=prices_IBM[i:i+10].std()
		upper=avg_10+std*2
		row.append(upper)
		lower=avg_10-std*2
		row.append(lower)
		bb=(prices_IBM[i+10]-avg_10)/2*std
		row.append(bb)
		rs.append(row)
	colname=['Date','Price','10-Days-AVG','UPPER CURVE','LOWER CURVE','BollingerBand']
	rs = pd.DataFrame(rs[0:],columns=colname)
	#print rs

	if gen_plot:
		rs.plot(x='Date',fontsize=14)
		plt.show()
	return rs
if __name__ == "__main__":
	cal_bb(gen_plot=True)
