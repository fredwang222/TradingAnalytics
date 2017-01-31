import datetime as dt
from util import get_data, plot_data
import math
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import string
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

def EMA(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), \
    syms = ['IBM'],N = 19):
	dates = pd.date_range(sd, ed)
	prices_all = get_data(syms, dates)  
	prices = prices_all[syms]  
	prices_IBM = prices_all['IBM']
	rs = []
	alpha = 2.0/(N+1)
	appk = 3.45*(N+1)
	ema0 = 0
	for i in range(0,N):
		ema0+=((1-alpha)**(i-1))*prices_IBM[i]
	ema0 = ema0*alpha
	rs.append([prices_IBM.index[N],prices_IBM[N],ema0])
	for i in range(1,len(prices_IBM[N:])):
		row=[]
		time=prices_IBM.index[i+N]
		row.append(time)
		currentP = prices_IBM[i+N]
		row.append(currentP)
		ema = (currentP*alpha)+(ema0*(1-alpha))
		ema0 = ema
		row.append(ema)
		rs.append(row)
	
	#colname=['Date','Price','EMA']	
	#rs = pd.DataFrame(rs[0:],columns=colname)
	#print rs

	return rs

def cal_MACD(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), \
    syms = ['IBM'],gen_plot=False):
	#READ IN DATA
	EMA12 = EMA(sd,ed,syms,N=12)
	EMA26 = EMA(sd,ed,syms,N=26)
	

	#print len(EMA12)
	#timestart=EMA26['Date'][0]
	#print timestart
	#timestart = pd.Timestamp(timestart)
	EMA12 = EMA12[14:]
	tempd = []
	for i in range(0,len(EMA12)):
		difi = EMA12[i][-1]-EMA26[i][-1]
		tempd.append(difi)
		#print difi
	emax = 0
	for i in range(0,9):
		emax += ((1-(2.0/11))**(i-1))*tempd[i]
		#print emax
	emai = emax * (2.0/11)
	#print emai
	dem =[]
	for i in range(9,len(tempd)):
		ema = (tempd[i]*(2.0/11))+(emai*(1-(2.0/11)))
		emai= ema
		dem.append(ema)
		#print ema
	#print "DEMLEN",len(dem)
	#print "DEm12",len(EMA12)
	#print "DEM26",len(EMA26)
	EMA12 = EMA12[9:]
	EMA26 = EMA26[9:]
	#print "DEMLEN",len(dem)
	#print "DEm12",len(EMA12)
	#print "DEM26",len(EMA26)

	rs = []
	
	
	for i in range(0,len(EMA12)):
		row=[]
		#print EMA12[i][-1]
		price = EMA12[i][-2]
		#price2 = EMA26[i][-2]
		#print price,price2
		DIF = EMA12[i][-1]-EMA26[i][-1]
		demtmp = dem[i]
		osc = DIF-demtmp
		#print dem
		#print DIF
		row.append(EMA12[i][0])
		row.append(price)
		row.append(DIF)
		row.append(demtmp)
		row.append(osc)
		rs.append(row)
	colname=['Date','Price','DIF','DEM','OSC']
	rs = pd.DataFrame(rs[0:],columns=colname)
	#print rs
	if gen_plot:
		prs = rs.set_index('Date')
		#prs['OSC'].plot(x='Date',fontsize=14)
		prs['DIF'].plot(x='Date',fontsize=14)
		prs['DEM'].plot(x='Date',fontsize=14)
		plt.legend(loc='best')
		plt.show()
	#print rs
	return rs



