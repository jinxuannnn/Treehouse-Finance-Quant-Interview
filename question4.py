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


#qns4c Portfolio Optimisation, generating efficient frontier and maximising Sharpe Ratio
num_portfolios = 30000

#generating random portfolios with different weights
def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights ) *365
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(365)
    return std, returns

def random_portfolios(num_portfolios, avg_rets, cov_matrix):
    results = np.zeros((3,num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        #Generating random weights
        weights = np.random.random(7)
        #normalising weights
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, avg_rets, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = portfolio_return  / portfolio_std_dev
    return results, weights_record

def display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios):
    #Generating 30000 random weights, saving their returns, std dev, sharpe ratio
    results, weights = random_portfolios(num_portfolios,mean_returns, cov_matrix) 

    #finding index of max sharpe ratio
    max_sharpe_idx = np.argmax(results[2])
    #getting the returns and std dev of this particular portfolio
    sdp, rp = results[0,max_sharpe_idx], results[1,max_sharpe_idx]
    #allocation of weights with max sharpe ratio
    max_sharpe_allocation = weights[max_sharpe_idx]

    #finding index of min volatility/standard deviation
    min_vol_idx = np.argmin(results[0])
    #getting the returns and std dev of this particular portfolio
    sdp_min, rp_min = results[0,min_vol_idx], results[1,min_vol_idx]
    #allocation of weights with min volatility/standard deviation
    min_vol_allocation = weights[min_vol_idx]  
    
    #finding index of max returns
    max_returns_idx = np.argmax(results[1])
    #getting the returns and std dev of this particular portfolio
    sdp_max, rp_max = results[0,max_returns_idx], results[1,max_returns_idx]
    #allocation of weights with max returns
    max_returns_allocation = weights[max_returns_idx]  
    
    print(f'''Max sharpe ratio portfolio return: {round(rp,2)}
Volatility: {round(sdp,2)}
{max_sharpe_allocation}''')
    print('-'*18)
    print(f'''Min volatility portfolio return: {round(rp_min,2)}
Volatility: {round(sdp_min,2)}
{min_vol_allocation}''')
    print('-'*18)
    print(f'''Max returns: {round(rp_max,2)}
Volatility: {round(sdp_max,2)}
{max_returns_allocation}''')

display_simulated_ef_with_random(avg_rets, cov_matrix, num_portfolios)
# output
# Max sharpe ratio portfolio return: 0.32
# Volatility: 0.2
# [0.04270409 0.34324545 0.00436848 0.01489951 0.28455692 0.02515885
#  0.2850667 ]
# ------------------
# Min volatility portfolio return: 0.14
# Volatility: 0.15
# [0.03511302 0.1982911  0.15794914 0.02835736 0.2054005  0.37117518
#  0.00371369]
# ------------------
# Max returns: 0.37
# Volatility: 0.25
# [0.04935525 0.06067908 0.08015331 0.05189512 0.09388982 0.02189946
#  0.64212796]
# Note: weights are ordered according to ['AAPL','IBM', 'GOOG', 'BP','XOM','COST','GS']
# Not sure how to incorporate shorting and rebalancing monthly. I would think shorting will be able to reduce volatility further
# and being able to rebalance monthly allows change of portfolio weights from the new month data. Using the new data to find
# the updated efficient frontier for max sharpe/returns/min risk.

#Answer: I would choose my optimal portfolio weights to be one that maximises the sharpe ratio, max returns per unit risk
# However, if an investor wants to maximise returns or minimise risk, the investor can choose either of the other two weights. 
