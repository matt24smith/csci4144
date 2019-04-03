import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Read in the data
df = pd.read_excel('Online_Retail.xlsx', index_col=0)
dfb = pd.read_csv('bloodstockSalesData.csv', index_col=0)

#-------------------------------------------------------------
#DATA PREPROCESSING

#Create year, month and qurter from InvoiceDate date column
df['Year'] = pd.DatetimeIndex(df['InvoiceDate']).year
df['Month'] = pd.DatetimeIndex(df['InvoiceDate']).month
df['Quarter'] = pd.DatetimeIndex(df['InvoiceDate']).quarter

#Create revenue column. Profit is quantity * unit price
df['Revenue'] = df['Quantity'] * df['UnitPrice']

#Create year, month and qurter from InvoiceDate date column
dfb['Year'] = pd.DatetimeIndex(dfb['saleDate']).year
dfb['Month'] = pd.DatetimeIndex(dfb['saleDate']).month
dfb['Quarter'] = pd.DatetimeIndex(dfb['saleDate']).quarter

#-------------------------------------------------------------
#DISPLAYING DATA

#Revenue by Month
monthly_data = df.groupby(['Year', 'Month'])['Revenue'].sum()
monthly = list(monthly_data)

#Revenue by Quarter
quarter_data = df.groupby(['Year', 'Quarter'])['Revenue'].sum()
quarter = list(quarter_data)

#Revenue by Month for bloodstock
monthly_datab = dfb.groupby(['Year', 'Month'])['Price'].sum()
monthlyb = list(monthly_datab)

#Revenue by Quarter
quarter_datab = dfb.groupby(['Year', 'Quarter'])['Price'].sum()
quarterb = list(quarter_datab)

#plot the total sales per month
# It is seen that this data is seasonal
plt.plot(monthlyb, 'bo-') 
plt.plot(quarterb, 'bo-') 
#-------------------------------------------------------------
# METHODS FOR DETERMING THE NEXT POINT IN THE SERIES...
# Method 1: Arithmetic mean
def avg(series):
    s = sum(series)
    l = len(series)
    return float(s/l)

# Method 2: Moving average. Average over the last n points in the series.
def moving_avg(series, n):
    return avg(series[-n:])
    
# Method 3:Weighted moving average. 
# Points are weighted so that some contribute more to the calculation.
# Weights is a list of weights that add up to 1. ex: [0.2, 0.3, 0.4, 0.1]
def weighted_avg(series, weights):
    avg = 0.0
    weights.reverse()
    for n in range(len(weights)):
        avg += series[-n-1] * weights[n]
    return avg

# Method 4: Exponential smoothing.
# Calculates the next point using the formula: alpha*y_x + (1-alpha)*y_x-1
# Where y_x is the current value in the seires, y_x-1 is the expected value 
# of the previous point in the series, and alpha is a value between 0-1
# For our series, a higher value of alpha (0.9) seems to work best
def exponential_smoothing(series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

# Method 5: Double exponential smoothing
# Calculates the next point using three formulas: one for trend, one for level
# and one for the forecast
def double_exponential_smoothing(series, alpha, beta):
    result = [series[0]]
    #To forecast 2 points, change len(series)+1 to len(series)+2
    for n in range(1, len(series)+1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series): # forecasting
          value = result[-1] # last value computed in result
        else:
          value = series[n]
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
    return result

#Method 6: Triple exponential smoothing
#-------------------------------------------------------------
# GRAPHING METHODS