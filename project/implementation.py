import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


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

def input_alpha(prompt):
    while True:
        try: 
            alpha = float(input(prompt))
            assert(alpha >= 0)
            assert(alpha <= 1)
            return alpha
        except : 
            print("Invalid alpha")

def input_stockID(prompt, df):
    while True:
        try:
            stockID = input(prompt)
            try:
                stockID = int(stockID)
            except:
                pass
            assert(stockID in np.array(df['StockCode']))
            return stockID
        except:
            print("Invalid Stock Code: item not found in dataset")


print("Reading information from Online_Retail.xlsx ...")
df = pd.read_excel('Online_Retail.xlsx', index_col=0)

df['Year'] = pd.DatetimeIndex(df['InvoiceDate']).year
df['Month'] = pd.DatetimeIndex(df['InvoiceDate']).month
df['Quarter'] = pd.DatetimeIndex(df['InvoiceDate']).quarter
df['Revenue'] = df['Quantity'] * df['UnitPrice']

def graph(df):
    alpha = input_alpha("Input an alpha value for double exponential smoothing.\n0 <= alpha <= 1 (Default: 0.5) : ")
    stockID = input_stockID("Input a stock code to aggregate on (Default: 23077 for lipgloss stock item) : ", df)

    # donut lip gloss: stock code=23077
    item_df_all = df[df['StockCode'] == stockID]
    item_df = item_df_all[item_df_all['Year'] == 2011]
    item_monthly_withdecember = item_df.groupby(['StockCode', 'Year', 'Month'])['Revenue'].sum()  # aggregate
    item_monthly = item_monthly_withdecember[:-1]
    item_xlabels = [str(x) for x in item_monthly.index.levels[2]][:-1]
    beta = alpha
    smoothed_monthly_item = double_exponential_smoothing(item_monthly, alpha, beta)

    # plotting for stock item
    fig = plt.figure("monthly")
    fig.suptitle(item_df['Description'][0] + " - Sales by Month")
    salesplt,  = plt.plot(item_xlabels,             list(item_monthly),                 'o-', c="xkcd:deep blue") 
    predicplt, = plt.plot(item_xlabels[-1:]+['12'], list(smoothed_monthly_item)[-2:],   'o-', c="xkcd:goldenrod") 
    smoothplt, = plt.plot(item_xlabels,             list(smoothed_monthly_item)[:-1],   'o-', c="xkcd:red") 
    plt.legend([salesplt, smoothplt, predicplt], ["Observed", "Smoothed: alpha=%s"%(alpha), "Predictions: alpha=%s"%(alpha)])
    plt.xlabel("Month (2011)")
    plt.xticks(item_xlabels + ['12'])
    plt.ylabel("Sales")
    plt.savefig(item_df['Description'][0] + "_monthly.png", bbox_inches='tight')
    plt.close()
    print("Results saved to " + item_df['Description'][0] + "_monthly.png")

graph(df)
again = input("Would you like to plot another stock item? [y/n] :")
while (again[0] == "y" or again[0] == "Y"):
    graph(df)
    again = input("Would you like to plot another stock item? [y/n] :")

