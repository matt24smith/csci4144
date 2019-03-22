import pandas as pd
import numpy as np
import os

#load in data

min_sup = float(input("\nEnter a minimum support  "))

def writeline():
    with open("data.txt", 'a') as f:
        f.write("\n")

def BUC(inpt, dim):
    outputRec = inpt
    writeline()
    dim_dic = {}
    for i in set(inpt.columns):
        if (i == 'Sales_Units'): continue
        dim_dic[(i)] = len(inpt[i].unique())
    numDims = 4
    for d in range(dim, numDims):
        dimName = list(dim_dic.keys())[d]
        C = dim_dic[dimName]  # (6) create C partitions of data for dimension d
        k=0
        for i in range (0, C): # i is the partition index...
            c = inpt.groupby([dimName]).count().values[i][0]
            cond = inpt.groupby([dimName])['Sales_Units'].sum().values[i]
            if cond >= min_sup:
                nextInpt = df.iloc[k:k+c-1]
                dim = dim + 1
                BUC(nextInpt, dim)
            k += c
    return outputRec

try:
    os.remove("data.txt")
except:
    print()

df = pd.read_csv('Product_Sales_Data_Set.csv', sep=',')
output = BUC(df, 0)
output.to_csv('data.txt', header=True, index=True, sep='\t', mode='a')


# step 1:
# readme file

# step 2:
# get minimum support from the input

# step 3:
# calculate the BUC function

# step 4:
# save the results in a file (csv)
# easy if you have a df: df.to_csv("output.csv") 

# step 5:
# ???

# step 6:
# profit!
