"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo



# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms] 
    # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocsguess = []
    for i in range(0,len(syms)):
        allocsguess.append(1.0/len(syms))
    # add code here to find the allocations
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    sv = 1000000
    sf = 252   
    # Get daily portfolio value
    #port_val = prices_SPY # add code here to compute daily portfolio values
    allocs = np.array(allocsguess)
    
    bnds = []
    for i in range (0,len(syms)):
        bnds.append((0,1.0))
    bnds = tuple(bnds)


    def SharpeRatio(allocs):
        sf = 252
        normed = prices/prices.ix[0,]
        alloced = normed * allocs
        pos_vals = alloced * sv
        port_val = pos_vals.sum(axis=1)
        cr = (port_val[-1]/port_val[0])-1
        daily_ret = (port_val/port_val.shift(1))-1
        adr = daily_ret.mean()
        sddr = daily_ret.std()
        sr = (adr-0)/(sddr)*np.sqrt(sf)
        return -sr
    #Call the optimizer
    result = spo.minimize(SharpeRatio,allocsguess,bounds = bnds,constraints = ({'type':'eq','fun': lambda allocs: 1.0 - np.sum(allocs)}))
    ##Print out the optimizing result
    #print result.x

    allocs = result.x
    normed = prices/prices.ix[0,]
    alloced = normed * allocs
    pos_vals = alloced * sv
    port_val = pos_vals.sum(axis=1)
    cr = (port_val[-1]/port_val[0])-1
    daily_ret = (port_val/port_val.shift(1))-1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    sr = (adr-0)/(sddr)*np.sqrt(sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        dfspy = df_temp['SPY']/df_temp['SPY'].ix[0,]
        dfport = df_temp['Portfolio']/df_temp['Portfolio'].ix[0,]
        spyplot = dfspy.plot(title = "Normalized SPY", label="SPY")
        portplot = dfport.plot(title = "Normalized Portfolio", label="Portfolio")
        spyplot.yaxis.grid(color='gray', linestyle='dashed')
        spyplot.xaxis.grid(color='gray', linestyle='dashed')
        spyplot.set_xlabel("Date")
        spyplot.set_ylabel("Normalized Values")
        spyplot.legend(loc = 'upper left')
        plt.show()
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    symbols = ['IBM', 'X', 'HNZ', 'XOM', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
