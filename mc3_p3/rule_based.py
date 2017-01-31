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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def cal_conservative(bbdata,mtdata,macddt):
     rs = 0
     if bbdata.iloc[5] <= -1.0:
          rs+=0.8
     if bbdata.iloc[5] >= 1.0:
          rs -=0.8
     if mtdata.iloc[3] >0.05:
          rs+=0.2
     if mtdata.iloc[3]<= -0.05:
          rs-=0.2
     if macddt.iloc[2]-macddt.iloc[3]<0 and abs (macddt.iloc[2]-macddt.iloc[3])<=0.1:
          if macddt.iloc[4] < 0:
               rs+=0.5
          else:
               rs+=1
     if macddt.iloc[2]-macddt.iloc[3]>0 and abs (macddt.iloc[2]-macddt.iloc[3])<=0.1:
          if macddt.iloc[4] > 0:
               rs -= 0.5
          else:
               rs-= 1
     if -1.0<=bbdata.iloc[5] and bbdata.iloc[5]<= -1.0:
          if rs>0.4:
               rs = 1
          if rs<-0.4:
               rs = -1
     if rs==0:
          if bbdata.iloc[5] >=0:
               rs = -0.5+0.1*macddt.iloc[4]
          if bbdata.iloc[5]<=0:
               rs = 0.5-0.1*macddt.iloc[4]


     return rs

def cal_RBT(bbdata,mtdata,macddt,sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31),fund=100000,gen_plot=True):
     dates = pd.date_range(sd, ed)
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
     consevative = 0
     while i <=(len(bbdata)-10):
          consevative = cal_conservative(bbdata.iloc[i],mtdata.iloc[i],macddt.iloc[i])
          #print consevative
          if consevative >= 0.6:
               exet=str(bbdata.iloc[i][0])
               dateexe = dateutil.parser.parse(exet).date()
               order.append([dateexe,"IBM","BUY",500])
               i=i+10
               exet=str(bbdata.iloc[i][0])
               dateexe = dateutil.parser.parse(exet).date()
               order.append([dateexe,"IBM","SELL",500])
          elif consevative<=-0.6:
               exet=str(bbdata.iloc[i][0])
               dateexe = dateutil.parser.parse(exet).date()
               order.append([dateexe,"IBM","SELL",500])
               i=i+10
               exet=str(bbdata.iloc[i][0])
               dateexe = dateutil.parser.parse(exet).date()
               order.append([dateexe,"IBM","BUY",500])
          else:
               i=i+1
               
     with open("RBTraderorder.csv", "wb") as f:
          writer = csv.writer(f)
          writer.writerow(["Date","Symbol","Order","Shares"])
          for item in order:
               writer.writerow([item[0],item[1],item[2],item[3]])
     f.close()

     if gen_plot:
          st=mk.compute_portvals("RBTraderorder.csv",start_val=100000)
          st.columns=['RuleBased']
          IBM_BENCHMARK = pd.DataFrame(port_val_rs)
          IBM_BENCHMARK.columns=['IBM_BENCHMARK']
          result = pd.concat([IBM_BENCHMARK, st], axis=1)
          result.loc[:,'IBM_BENCHMARK'] /= fund
          result.loc[:,'RuleBased'] /= fund
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
     

def RBtest_code(sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31)):
     BBdata = bb.cal_bb(sd=sd,ed=ed)
     MTdata = mt.cal_momentum(N=2,sd=sd,ed=ed)
     MACDdt = macd.cal_MACD(sd=sd, ed=ed )
     MACDdt.set_index(['Date'])
     fd =  MACDdt['Date'][0]
     mask1 = (BBdata['Date'] >= fd)
     mask2 = (MTdata['Date']>=fd )
     BBdata= BBdata.loc[mask1]
     MTdata = MTdata.loc[mask2]
     #print BBdata.shape
     #print MTdata.shape
     #print MACDdt.shape
     rs = cal_RBT(bbdata = BBdata,mtdata=MTdata,macddt=MACDdt,sd=sd,ed=ed)
     return rs

def import3dataframe(sd=dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31)):
     BBdata = bb.cal_bb(sd=sd,ed=ed)
     MT2data = mt.cal_momentum(N=2,sd=sd,ed=ed)
     MT10data = mt.cal_momentum(N=10,sd=sd,ed=ed)
     MACDdt = macd.cal_MACD(sd=sd, ed=ed )
     MACDdt.set_index(['Date'])
     fd =  MACDdt['Date'][0]
     mask1 = (BBdata['Date'] >= fd)
     mask2 = (MT2data['Date']>=fd )
     mask3 = (MT10data['Date']>=fd)
     BBdata= BBdata.loc[mask1]
     MT2data = MT2data.loc[mask2]
     MT10data = MT10data.loc[mask3]
     #print BBdata.shape
     #print MTdata.shape
     #print MACDdt.shape
     return BBdata,MT2data,MT10data,MACDdt

if __name__ == "__main__":
     RBtest_code()



