"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch    modified by Yuzhou Li
"""

import datetime as dt
import QLearner as ql
import pandas as pd
import util as ut
import copy
import itertools
import math
import csv
import marketsim as mk
import matplotlib.pyplot as plt

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.learner = None



    def discretize(self,inputvector,numberofparts):
        if isinstance (inputvector,pd.DataFrame):
            s = inputvector.values.tolist()
            #print type(s)
            inputvector = list(itertools.chain.from_iterable(s))
        inputvector.sort()
        sort = copy.copy(inputvector)
        #print sort
        sort.reverse()
        length = len(inputvector)
        pkglen = int(math.floor(length/numberofparts))
        rs = []
        for i in range(0,numberofparts-1):
            temp =[]
            for j in range(0,pkglen):
                temp.append(sort.pop())
            rs.append(temp)
        sort.reverse()
        rs.append(sort)
        return rs


    def getVectorStateNumber(self,disvector,number):
        lenofvec = len(disvector)
        for i in range(0,lenofvec):
            tmpmin = disvector[i][0]
            tmpmax = disvector[i][-1]
            if tmpmin<=number<=tmpmax:
                return i
        return "THIS NUMBER IS GREATER THAN SAMPLE"
    


    # this method should create a QLearner, and train it for trading
    

    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2006,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000): 

        # add your code to do learning here

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        numberofdays = len(prices)
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices

        #Compute the rolling mean
        rollingmean = pd.rolling_mean(prices,window=14)
        rollingstd = pd.rolling_std(prices,window=14)
        #Compute the 10 day momentum

        MM = prices.copy()

        MM.values[14:]-= prices.values[:-14]
        MM.values[14:]/= prices.values[:-14]
        listMM = list(itertools.chain.from_iterable(MM.values[14:].tolist()))
        #print listMM
        #Compute Bollinger Band %b index
        BB = (prices-rollingmean)/(2*rollingstd)
        #Compute RSI
        Pricecopy2 = prices.copy()
        delta = Pricecopy2.diff()
        U = delta.copy()
        D = delta.copy()
        U[U<0]=0
        D[D>0]=0
        rollup = pd.stats.moments.ewma(U, 14)
        rolldown = pd.stats.moments.ewma(D.abs(), 14)
        RS = rollup/rolldown
        RSI = 100.0-(100.0/(1.0 + RS))
        #print RSI

        #GENERATE DISCRETIZING COMPONENT
        listBB = list(itertools.chain.from_iterable(BB.values[14:].tolist()))
        #print len(listBB)
        BBDIS = self.discretize(listBB,10)
        MMDIS = self.discretize(listMM,10)
        listRSI = list(itertools.chain.from_iterable(RSI.values[14:].tolist()))
        RSIDIS = self.discretize(listRSI,4)
        self.learner = ql.QLearner(num_states=400,num_actions=3)
        currentholding = 0
        #Initialize the 
        print BB
        enum1 = self.getVectorStateNumber(BBDIS,BB.values[14])
        #print type(enum1)
        enum2 = self.getVectorStateNumber(MMDIS,MM.values[14])
        #print type(enum2)
        enum3 = self.getVectorStateNumber(RSIDIS,RSI.values[14])
        #print type(enum3)
        state = 100*enum3+10*enum2+enum1
        #print state
        iniaction = self.learner.querysetstate(state)
        #print iniaction #IF 2 BUY, 1 DO NOTHING, 0 SELL
        currentholding += 500*(iniaction-1)
        for iteri in range(0,200):
            cumulativereward = 0
            for i in range(15,numberofdays):
                enum1 = self.getVectorStateNumber(BBDIS,BB.values[i])
                enum2 = self.getVectorStateNumber(MMDIS,MM.values[i])
                enum3 = self.getVectorStateNumber(RSIDIS,RSI.values[i])
                state= 100*enum3+10*enum2+enum1
                currentreward = currentholding*(prices.values[i]-prices.values[i-1])
                cumulativereward+=currentreward
                nextaction = self.learner.query(state,currentreward)
                if currentholding==500:
                    if nextaction == 0:
                        currentholding -= 1000 #SELL TWO TIMES
                elif currentholding ==0:
                    currentholding += 500*(nextaction-1) #NORMAL OPERATION
                elif currentholding == -500:
                    if nextaction == 2:
                        currentholding += 1000 #BUY SIGNAL

        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume
        #print "THIS IS Q TABLE\n",self.learner.Q
        #print len(listRSI),len(listBB),len(listMM)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2010,12,31), \
        sv = 100000):

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        numberofdays = len(prices)
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0 # set them all to nothing
        if self.verbose: print prices 
        benchmarkprice = prices_all[[symbol]]
        firstbuy=(benchmarkprice[symbol][0])*500 #VALUE CAN BE CHANGED TO ANY
        money = sv - firstbuy
        port_val_rs=[] #Benchmark
        for index,price in benchmarkprice.iterrows():
            port_val = money + price * 500
            port_val_rs.append(port_val)
        #BENCHMARK END
        rmOut=pd.rolling_mean(prices,window=14)
        rstdOut=pd.rolling_std(prices,window=14)
        #print "rmOut",rmOut
        #Compute BB index
        BBOut = (prices-rmOut)/(2*rstdOut)
        #print "bbOut",BBOut
        #Compute Momentum
        MMOut = prices.copy()
        MMOut.values[14:]-= prices.values[:-14]
        MMOut.values[14:]/= prices.values[:-14]
        listMMOut = list(itertools.chain.from_iterable(MMOut.values.tolist()))
        #print listMMOut
        #Compute RSI
        Pricecopy2 = prices.copy()
        delta = Pricecopy2.diff()
        U = delta.copy()
        D = delta.copy()
        U[U<0]=0
        D[D>0]=0
        rollup = pd.stats.moments.ewma(U, 14)
        rolldown = pd.stats.moments.ewma(D.abs(), 14)
        RS = rollup/rolldown
        RSIOut = 100.0-(100.0/(1.0 + RS))
        listMMOut = list(itertools.chain.from_iterable(MMOut.values[14:].tolist()))
        #print "THIS IS LIST MMOUT",type(listMMOut[3])
        listBBOut = list(itertools.chain.from_iterable(BBOut.values[14:].tolist()))
        listRSIOut = list(itertools.chain.from_iterable(RSIOut.values[14:].tolist()))
        #DISCRETIZE
        BBDISOut = self.discretize(listBBOut,10)
        #print BBDISOut
        MMDISOut = self.discretize(listMMOut,10)
        RSIDISOut = self.discretize(listRSIOut,4)
        #THIS IS QUERY PART
        stockholding = 0
        for i in range(14,numberofdays):
            #print "BBVALUETYPE",BBOut.values[i]
            enum1 = self.getVectorStateNumber(BBDISOut,BBOut.values[i])
            #print "ENUM1\n",enum1
            enum2 = self.getVectorStateNumber(MMDISOut,MMOut.values[i])
            #print "ENUM2\n",enum2
            enum3 = self.getVectorStateNumber(RSIDISOut,RSIOut.values[i])
            #print "ENUM3\n",enum3
            state= 100*enum3+10*enum2+enum1
            #print state
            #print type(state)
            act = self.learner.querysetstate(state)
            if stockholding==500:
                if act == 0:
                    stockholding -= 1000 #SELL TWO TIMES
                    trades.values[i,:]= -1000
            elif stockholding ==0:
                stockholding += 500*(act-1) #NORMAL OPERATION
                trades.values[i,:] = 500*(act-1)
            elif stockholding == -500:
                if act == 2:
                    stockholding += 1000 #BUY SIGNAL
                    trades.values[i,:] = 1000
        # here we build a fake set of trades
        # your code should return the same sort of data
        #dates = pd.date_range(sd, ed)
        #prices_all = ut.get_data([symbol], dates)  # automatically adds SPY


        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        #print trades.index
        #GENERATE ORDER FILE
        with open("Order.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(["Date","Symbol","Order","Shares"])
            for row in trades.iterrows():
                #print row.index
                if row[1].values>=0:
                    action = "BUY"
                else:
                    action = "SELL"
                writer.writerow([row[0].date(),symbol,action,abs(int(row[1].values))])
        f.close()
        #BENCHMARK
        print pd.DataFrame(port_val_rs)
        #GENERATE PLOTS
        st=mk.compute_portvals("Order.csv",start_val=sv)
        st.columns=['QLearnerOrder']
        BENCHMARK = pd.DataFrame(port_val_rs)
        BENCHMARK.columns=['BENCHMARK']
        result = pd.concat([BENCHMARK, st], axis=1)
        result.loc[:,'BENCHMARK'] /= sv
        result.loc[:,'QLearnerOrder'] /= sv
        result.plot(fontsize=12,color=['black','blue'])
        plt.show()


        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
    SL = StrategyLearner()
    SL.addEvidence()
    SL.testPolicy()
