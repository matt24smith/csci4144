# Data Mining - Assignment 3
# Matthew Smith
# 2019-03-29

# Some references were used in the completion of this assignment
# Please see Readme.txt for more details

import numpy as np
filename = "Play_Tennis_Data_Set.csv"
stringArray = np.loadtxt(filename, skiprows=1, delimiter=",", dtype=str)
stringArray = np.array([list(x) for x in stringArray])

labelmap = {
    "sunny"     : 1,
    "overcast"  : 2,
    "rain"      : 3,
    "hot"       : 4,
    "mild"      : 5,
    "cool"      : 6,
    "high"      : 7,
    "normal"    : 8, 
    "FALSE"     : 9,
    "TRUE"      : 10,
    "N"         : 11,
    "P"         : 12,
}
intmap = {v : k for k, v in labelmap.items()}

inputArray = np.array([[labelmap[x] for x in y] for y in stringArray])
inputList = [list(x) for x in inputArray]

def genCk(Lk, k):
    # generates array of candidate sets
    output = []
    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if (L1 == L2):
                output.append(Lk[i] | Lk[j])
    return output

def scanD(D, Ck, minsup):
    # compares support to minimum support
    count = {}
    for tid in D:
        for can in Ck: 
            print(can)
            print(tid)
            if set(can).issubset(set(tid)):
                #if not can in count: count[can] = 1
                #else: count[can] += 1
                for item in can:
                    if not item in count: count[item] = 1
                    else: count[item] += 1
    lenD = float(len(D))
    output = []
    supportdata = {}
    for key in count:
        support = count[key] / lenD 
        if support >= minsup:
            output.insert(0, key);
        supportdata[key] = support
    return output, supportdata

def apriori(C1, minsup=0.5):
    # C1 is the input dataset in list format
    D = list(map(set, C1))
    L1, supportdata = scanD(D, C1, minsup)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = genCk(L[k-2], k)
        Lk, supK = scanD(D, Ck, minsup)
        supportdata.update(supK)
        L.append(Lk)
        k += 1
    return L, supportdata

minsup = float(input("Please input minumum support value.\n"
    + "Valid range includes float values between 0 and 1.\n"
    + "minsup = "))

L.suppdata = apriori(inputList)

print(L)
