# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Standard Imports
import sys

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Assumed Trading days to be 252 as per wiki. Ideally must be len(data)
TRADING_DAYS = 252

# 
def simulate(close_price, initial_allocations):
    # Convert Start time and end time to date time objects
    
    equity_returns = close_price.copy() * initial_allocations
    
    portfolio_return = np.sum(equity_returns, axis = 1)
    
    cumulative_return = portfolio_return[-1]
    
    tsu.returnize0(portfolio_return)
    
    port_std_dev = np.std(portfolio_return)
    port_avg_return = np.average(portfolio_return)
    
    sharpe_ratio = np.sqrt(TRADING_DAYS)*(port_avg_return/port_std_dev)
    
    return port_std_dev, port_avg_return, sharpe_ratio, cumulative_return


def allocations():
    all_combinations = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    combinations = []
    
    for i in all_combinations:
        for j in all_combinations:
            for k in all_combinations:
                for l in all_combinations:
                    if i + j + k + l == 1.0:
                        combinations.append([i, j, k, l])
    return combinations
if __name__ == '__main__':

    equity_symbols =  ['BRCM', 'TXN', 'AMD', 'ADI']  
    start_date = '2010-01-01'
    end_date = '2010-12-31'
    start_date = (dt.datetime.strptime(start_date, '%Y-%m-%d')).date()
    end_date = (dt.datetime.strptime(end_date, '%Y-%m-%d')).date()
    
    # Time of day delta object
    timeOfDay = dt.timedelta(hours = 16)
    
    # Create data access object
    dataObj = da.DataAccess('Yahoo')
    
    #Obtain all the trading days 
    tradingDays = du.getNYSEdays(start_date, end_date, timeOfDay)
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    
    data = dataObj.get_data(tradingDays, equity_symbols, keys)
    dictData = dict(zip(keys, data))
    
    #Obtain the close values
    closeData = dictData['close'].values
    normalizedPrice = closeData/closeData[0,:]
        
    #Order -> sd, avg, sharp_ratio, cumulative_return
    optimal_result = [0.0, 0.0, 0.0, 0.0]
    optimal_allocation = []
    for allocation in allocations():
        print "Simulating Allocation: ", zip(equity_symbols, allocation)
        sd, avg, sharp_ratio, cum_ret = simulate(normalizedPrice, allocation)
        if sharp_ratio > optimal_result[2]:
            optimal_result = [sd, avg, sharp_ratio, cum_ret]
            optimal_allocation = allocation
        
    print "\n###### Optimal Allocation Details #########"
    print "Start Date: ", str(start_date)
    print "End Date: ", str(end_date)
    print "Equity Symbols: ", equity_symbols
    print "Optimal Allocation: ", optimal_allocation
    print "Volatality: ", optimal_result[0]
    print "Average Return: ", optimal_result[1]
    print "Sharpe Ratio: ", optimal_result[2]
    print "Cumulative Return: ", optimal_result[3]