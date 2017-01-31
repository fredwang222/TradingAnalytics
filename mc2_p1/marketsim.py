"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    orders_df = pd.read_csv(orders_file)   
    syms = orders_df.Symbol.unique()
    #print orders_df
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    start_date = orders_df['Date'].iloc[0]
    end_date = orders_df['Date'].iloc[-1]
    priceinfo = get_data(syms.tolist(), pd.date_range(start_date, end_date),addSPY=False)
    priceinfo = priceinfo.dropna(how='all')
    #print priceinfo

    #for items in priceinfo.iterrows():
    #    if np.isnan(items[1][1]) == False:
            
        
    leverage = 0
    currentPort= dict(zip(syms.tolist(),[0]*len(syms)))
    cash = start_val
    dailyportvlist = []

    for index, price in priceinfo.iterrows():
        portvals = cash
        for key,value in currentPort.iteritems():
            portvals = portvals + priceinfo.ix[index][key]*value
        dailyportvlist.append(portvals)
    
        if str(index.date()) in orders_df['Date'].values and str(index.date())!=str(dt.date(2011,6,15)):
            for idx, odr in orders_df[orders_df['Date']==str(index.date())].iterrows():
                absinv = 0
                inv = 0
                if odr.Order == "BUY":
                    currentPort[odr.Symbol] += odr.Shares
                    cash -= priceinfo.ix[odr.Date][odr.Symbol]*odr.Shares
                    for key,value in currentPort.iteritems():
                        absinv += abs(priceinfo.ix[odr.Date][key]*value)
                        inv += priceinfo.ix[odr.Date][key]*value
                    lev = absinv/(inv+cash)
                    if lev<=3.0:
                        leverage = lev
                    else: #Cancel the order because leverage exceeded
                        currentPort[odr.Symbol] -= odr.Shares
                        cash += priceinfo.ix[odr.Date][odr.Symbol]*odr.Shares
                else:
                    currentPort[odr.Symbol] -= odr.Shares
                    cash += priceinfo.ix[odr.Date][odr.Symbol]*odr.Shares
                    for key,value in currentPort.iteritems():
                        absinv += abs(priceinfo.ix[odr.Date][key]*value)
                        inv += priceinfo.ix[odr.Date][key]*value
                    lev = absinv/(inv+cash)
                    if lev<=3.0:
                        leverage = lev
                    else: #Cancel the order because leverage exceeded
                        currentPort[odr.Symbol] += odr.Shares
                        cash -= priceinfo.ix[odr.Date][odr.Symbol]*odr.Shares
    #print dailyportvlist
    return pd.DataFrame(data=dailyportvlist,index=priceinfo.index)



def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders3.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
        #print "ASASASASAS,\n",portvals
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]
    '''
    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])
    '''
if __name__ == "__main__":
    test_code()
