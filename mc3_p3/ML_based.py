import numpy as np
import datetime as dt
from util import get_data, plot_data
import math
import csv
import marketsim as mk
import dateutil
import datetime
import pandas as pd
#import matplotlib.pyplot as plt
import Bollinger_Band as bb
import momentum as mt
import MACD as macd
import BagLearner as bag
from rule_based import import3dataframe
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def createTrain(sd=dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31)):
	BBData,MT2Data,MT10Data,MACDData = import3dataframe(sd=sd,ed=ed)
	rs = []
	for i in range(0,len(BBData)-10):
		row = []
		row.append(BBData.iloc[i][1]) #Price
		row.append(BBData.iloc[i][2]) #10-Day-Avg
		row.append(BBData.iloc[i][3]) #UPBOUND
		row.append(BBData.iloc[i][4]) #LOBOUND
		row.append(BBData.iloc[i][5]) #BBINDEX
		row.append(MT2Data.iloc[i][3]) #2-day-momentum
		row.append(MT10Data.iloc[i][3]) #10-day-momentum
		row.append(MACDData.iloc[i][2]) #DIF
		row.append(MACDData.iloc[i][3]) #DEM
		row.append(MACDData.iloc[i][4]) #OSC
		row.append(BBData.iloc[i+10][1]) #10-day-after-price
		rs.append(row)

	rs = np.array(rs)
	TrainX = rs[:,0:-1]
	print TrainX.shape
	y = []
	for i in range(0,TrainX.shape[0]):
		if rs[i,-1]/rs[i,0]>=1.01:
			y.append(1)
		elif rs[i,-1]/rs[i,0]<=0.99:
			y.append(-1)
		else:
			y.append(0)
	TrainY = np.array(y)
	return TrainX,TrainY



def createTest(sd=dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31)):
	BBData,MT2Data,MT10Data,MACDData = import3dataframe(sd=sd,ed=ed)
	rs = []
	for i in range(0,len(BBData)-10):
		row = []
		row.append(BBData.iloc[i][1]) #Price
		row.append(BBData.iloc[i][2]) #10-Day-Avg
		row.append(BBData.iloc[i][3]) #UPBOUND
		row.append(BBData.iloc[i][4]) #LOBOUND
		row.append(BBData.iloc[i][5]) #BBINDEX
		row.append(MT2Data.iloc[i][3]) #2-day-momentum
		row.append(MT10Data.iloc[i][3]) #10-day-momentum
		row.append(MACDData.iloc[i][2]) #DIF
		row.append(MACDData.iloc[i][3]) #DEM
		row.append(MACDData.iloc[i][4]) #OSC
		row.append(BBData.iloc[i+10][1]) #10-day-after-price
		row.append(BBData.iloc[i][0]) #Time
		rs.append(row)

	rs = np.array(rs)
	TestX = rs[:,0:-2]
	return TestX,rs[:,-1]


def queryTest(sd,ed,TestYdata,Timelist,gen_plot=True,fund=100000):		
	dates = pd.date_range(sd,ed)
	syms=['IBM']
	prices_all = get_data(syms, dates)
	prices = prices_all[syms]
	firstbuy=(prices['IBM'][0])*500 
	money = fund - firstbuy     
	port_val_rs=[] #Benchmark
	for index,price in prices.iterrows():
	     port_val = money + price * 500
	     port_val_rs.append(port_val)
	order=[]
	port_val_list=[]
	i=0
	while i <=((TestYdata).shape[0]-11):
		temp = TestYdata[i]
		if temp == 1:
			exet=str(Timelist[i])
			dateexe = dateutil.parser.parse(exet).date()
			order.append([dateexe,"IBM","BUY",500])
			i=i+10
			exet=str(Timelist[i])
			dateexe = dateutil.parser.parse(exet).date()
			order.append([dateexe,"IBM","SELL",500])
		elif temp == -1:
			exet=str(Timelist[i])
			dateexe = dateutil.parser.parse(exet).date()
			order.append([dateexe,"IBM","SELL",500])
			i=i+10
			exet=str(Timelist[i])
			dateexe = dateutil.parser.parse(exet).date()
			order.append([dateexe,"IBM","BUY",500])
		else:
			i=i+1
	with open("RTTraderorder.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerow(["Date","Symbol","Order","Shares"])
		for item in order:
			writer.writerow([item[0],item[1],item[2],item[3]])
	f.close()

	if gen_plot:
		st=mk.compute_portvals("RTTraderorder.csv",start_val=100000)
		st.columns=['ML_Based']
		IBM_BENCHMARK = pd.DataFrame(port_val_rs)
		IBM_BENCHMARK.columns=['IBM_BENCHMARK']
		result = pd.concat([IBM_BENCHMARK, st], axis=1)
		#result=result.rename(columns = colname)
		result.loc[:,'IBM_BENCHMARK'] /= fund
		result.loc[:,'ML_Based'] /= fund
		result.plot(fontsize=12,color=['black','blue'])
		i=0
		while i <len(order):
			if order[i][2]=="BUY":
				plt.axvline(x=order[i][0], hold=None,color='g')
				i=i+1
				plt.axvline(x=order[i][0], hold=None,color='k')
				i=i+1
			elif order[i][2]=="SELL":
				plt.axvline(x=order[i][0], hold=None,color='r')
				i=i+1
				plt.axvline(x=order[i][0], hold=None,color='k')
				i=i+1
		plt.show()
	return result


def MLtest_code(sd=dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31)):
	TrainX,TrainY = createTrain()
	TestX,Timelist = createTest(sd,ed)
	#print Timelist
	bg = bag.BagLearner(kwargs = {"leaf_size":5,"verbose":False},bags = 20)
	bg.addEvidence(TrainX,TrainY)
	result = bg.query(TestX)
	TestY = np.array(result)
	rs = queryTest(sd,ed,TestYdata=TestY,Timelist= Timelist,gen_plot=True)
	return rs

if __name__ == "__main__":
	MLtest_code()


