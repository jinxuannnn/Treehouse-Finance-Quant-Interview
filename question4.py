import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import datetime as dt
from scipy.stats import norm
from matplotlib import pyplot as plt

#question4b
#Assumption that returns are normally distributed
#Assumption that initial investment is 100, can change it to 1 to find VaR in %

tickers = ['AAPL','IBM', 'GOOG', 'BP','XOM','COST','GS']
weights = np.array([.15, .20, .20, .15,.10,.15,.5])
initial_investment = 100

#pulling close prices from yahoo
data = pdr.get_data_yahoo(tickers, start="2016-01-01", end="2016-12-31")['Close']

#finding daily change of returns
returns = data.pct_change()
# print(returns.tail())

#finding cov matrix
cov_matrix = returns.cov()
# print(cov_matrix)

#finding mean of returns of the distribution
avg_rets = returns.mean()
#finding mean in % of portfolio returns
port_mean = avg_rets.dot(weights)
#finding std deviation of portfolio
port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
#finding absolute mean of portfolio w 100USD invested
mean_investment = (1+port_mean) * initial_investment
#finding std deviation of portfolio w 100USD invested
stdev_investment = initial_investment * port_stdev
#using alpha as 5%
conf_level1 = 0.05
#finding portfolio value at 5% left tail
cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)
#finding Value at Risk daily
var_1d1 = initial_investment - cutoff1
print(f'The value at risk for 1-day period is {np.round(var_1d1,2)} at 95% confidence interval')
#output 
#The value at risk for 1-day period is 2.39 at 95% confidence interval

#plotting Value at Risk for 365days
var_array = []
num_days = int(365)
for x in range(1, num_days+1):    
    var_array.append(np.round(var_1d1 * np.sqrt(x),2))
    # print(str(x) + " day VaR @ 95% confidence: " + str(np.round(var_1d1 * np.sqrt(x),2)))
#Value at Risk for 1 year period
print(f'The value at risk for 1 year period is {np.round(var_1d1 * np.sqrt(365),2)} at 95% confidence interval')
#output
#The value at risk for 1 year period is 45.64 at 95% confidence interval

# Build plot, graph is in question4Charts.md
plt.xlabel("Day #")
plt.ylabel("Max portfolio loss (USD)")
plt.title("Max portfolio loss (VaR) over 15-day period")
plt.plot(var_array, "r")


#finding conditional Value at Risk, expectation of the conditional prob that alpha occurs
#Not sure how to write the code to get the cVaR, my current output is 0
cVaR = 1/conf_level1 * norm.expect(lambda x: x, loc=mean_investment, scale=stdev_investment, lb=var_1d1)
print(cVaR)