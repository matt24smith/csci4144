import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_excel('Online_Retail.xlsx', index_col=0)

# Create columns 
df['Year'] = pd.DatetimeIndex(df['InvoiceDate']).year
df['Month'] = pd.DatetimeIndex(df['InvoiceDate']).month
df['Quarter'] = pd.DatetimeIndex(df['InvoiceDate']).quarter
df['Revenue'] = df['Quantity'] * df['UnitPrice']

#Revenue by time hierarchies
monthly_data = df.groupby(['StockCode', 'Year', 'Month'])['Revenue'].sum()
monthly = list(monthly_data)
quarter_data = df.groupby(['Year', 'Quarter'])['Revenue'].sum()
quarter = list(quarter_data)

# all items monthly 
fig = plt.figure("monthly")
plt.plot(monthly, 'bo-') 
plt.savefig("monthly.png")

# all items quarterly
fig = plt.figure("quarterly")
plt.plot(quarter, 'bo-') 
plt.savefig("quarterly.png")

# monthly for stock code 85049C
monthly_data_ribbons = monthly_data['85049C']
fig = plt.figure("monthly")
#fig.set_title("Romantic pinks ribbons sales by month")
plt.plot(list(monthly_data_ribbons), 'bo-') 
plt.savefig("monthly.png")
plt.close()

# donut lip gloss 23077
monthly_data_lipgloss = monthly_data[23077]
smoothed_monthly_lipgloss = double_exponential_smoothing(monthly_data_lipgloss, 0.5, 0.5)
fig = plt.figure("monthly")
fig.suptitle("Romantic pinks ribbons sales by month")
salesplt, = plt.plot(list(monthly_data_lipgloss), 'o-', c="blue", label="Sales Records") 
predicplt, = plt.plot([9, 10], list(smoothed_monthly_lipgloss)[-2:], 'o-', c="green", label="Smoothed Sales Records With Future Prediction") 
smoothplt, = plt.plot(list(smoothed_monthly_lipgloss)[:-1], 'o-', c="red", label="Smoothed Sales Records With Future Prediction") 
plt.legend([salesplt, smoothplt, predicplt], ["Observed", "Smoothed", "Predictions"])
plt.xlabel("Month")
plt.ylabel("Sales")
plt.savefig("monthly.png")
plt.close()

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
    """
    Series: list of values - e.g. sales data
    alpha: 0 > float > 1            0.1, 0.5, 0.9 are vals supplied in paper
    beta:  0 > float > 1 = alpha
        lower = optimism
        higher = pessimism 
    """
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
