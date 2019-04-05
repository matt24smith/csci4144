import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def avg(series):
    s = sum(series)
    l = len(series)
    return float(s/l)

def moving_avg(series, n):
    # avg last n points in series
    return avg(series[-n:])
    
def weighted_avg(series, weights):
    # Points are weighted so that some contribute more to the calculation.
    # Weights is a list of weights that add up to 1. ex: [0.2, 0.3, 0.4, 0.1]
    avg = 0.0
    weights.reverse()
    for n in range(len(weights)):
        avg += series[-n-1] * weights[n]
    return avg

def exponential_smoothing(series, alpha):
    # Calculates the next point using the formula: alpha*y_x + (1-alpha)*y_x-1
    # Where y_x is the current value in the seires, y_x-1 is the expected value 
    # of the previous point in the series, and alpha is a value between 0-1
    # For our series, a higher value of alpha (0.9) seems to work best
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def double_exponential_smoothing(series, alpha, beta):
    # Calculates the next point using three formulas: one for trend, one for level
    # and one for the forecast
    """
    Series: list of values - e.g. sales data
    alpha: 0 > float > 1            NOTE: 0.1, 0.5, 0.9 are vals supplied in paper
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


df = pd.read_excel('Online_Retail.xlsx', index_col=0)

df['Year'] = pd.DatetimeIndex(df['InvoiceDate']).year
df['Month'] = pd.DatetimeIndex(df['InvoiceDate']).month
df['Quarter'] = pd.DatetimeIndex(df['InvoiceDate']).quarter
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# aggregate revenue by stockcode and time hierarchies
#monthly_data = df.groupby(['StockCode', 'Year', 'Month'])['Revenue'].sum()
#monthly = list(monthly_data)

# donut lip gloss: stock code=23077
lipgloss_df = df[df['StockCode'] == 23077]
lipgloss_monthly_withdecember = lipgloss_df.groupby(['StockCode', 'Year', 'Month'])['Revenue'].sum()  # aggregate
lipgloss_monthly = lipgloss_monthly_withdecember[:-1]
lipgloss_xlabels = [str(x) for x in lipgloss_monthly.index.levels[2]][:-1]
alpha = 0.3
beta = alpha
smoothed_monthly_lipgloss = double_exponential_smoothing(lipgloss_monthly, alpha, beta)

# plotting for lip gloss
fig = plt.figure("monthly")
fig.suptitle("Donut Flavoured Lipgloss - Sales by Month")
salesplt,  = plt.plot(lipgloss_xlabels,             list(lipgloss_monthly),                 'o-', c="xkcd:deep blue") 
predicplt, = plt.plot(lipgloss_xlabels[-1:]+['12'], list(smoothed_monthly_lipgloss)[-2:],   'o-', c="xkcd:goldenrod") 
smoothplt, = plt.plot(lipgloss_xlabels,             list(smoothed_monthly_lipgloss)[:-1],   'o-', c="xkcd:red") 
plt.legend([salesplt, smoothplt, predicplt], ["Observed", "Smoothed: alpha=%s"%(alpha), "Predictions: alpha=%s"%(alpha)])
plt.xlabel("Month (2011)")
plt.xticks(lipgloss_xlabels + ['12'])
plt.ylabel("Sales")
plt.savefig("monthly_lipgloss.png", bbox_inches='tight')
plt.close()

