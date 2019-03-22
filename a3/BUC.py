import numpy as np

filename = "Product_Sales_Data_Set.csv"
stringArray = np.loadtxt(filename, skiprows=1, delimiter=",", dtype=str)
stringArray = np.array([list(x) for x in stringArray])

labelmap = {  # convert strings into integer labels
        "1"         : 1,
        "2"         : 2,
        "3"         : 3,
        "4"         : 4,
        "5"         : 5,
        "Computer"  : 6,
        "Camera"    : 7,
        "Phone"     : 8,
        "Printer"   : 9,
        "Toronto"   : 10,
        "Vancouver" : 11,
        "New York"  : 12,
        "Chicago"   : 13,
        "2017"      : 14,
        "2018"      : 15,
        "Samsung"   : 16,
        "Sony"      : 17,
        "HP"        : 18,
        "Dell"      : 19
    }
intmap = {v : k for k, v in labelmap.items()}
dimmap = {
        0 : "Item        ",
        1 : "Location    ",
        2 : "Year        ",
        3 : "Supplier    ",
        4 : "Sales       "
        }

inputArray = np.array([[labelmap[x] for x in y] for y in stringArray])

min_sup = float(input("minimum support = "))

def wh(s):  # add whitespace to print msg
    def _white(sp,ace):
        return _white(sp+" ",ace-1) if ace > 0 else sp
    return _white("",s)

def cubeslice(datacube, cubeix, prevsets, transpose=False):
    if transpose: datacube = datacube.T
    nextsets = []
    for s in prevsets:
        for value in np.unique(datacube[cubeix]):
            nextsets += [s[np.where(datacube[cubeix][s] == value)[0]]]
    if transpose: nextsets = np.array(nextsets).T
    return np.array(nextsets)

def aggregate(inputArray, dims, intmap, dimmap, min_sup):
    output = ""
    subsets = np.array([range(0, len(inputArray[:,0]))])
    for d in dims:
        subsets = cubeslice(inputArray.T, d, subsets, transpose=False)
    
    for d in range(0, 4): output += dimmap[d]
    output += wh(58-len(output)) + dimmap[4] + "\n"

    for s in subsets:
        if len(s) == 0: continue
        label = "  "
        for d in range(0, 4):
            labelitem = intmap[inputArray[s,d][0]]
            label += labelitem 
            label += wh(12-len(labelitem))
        aggsales = sum(inputArray[s,4])
        #if aggsales >= min_sup:
        output += (label + wh(60 - len(label)) + str(aggsales) + "\n")
    return output

def partition(inputArray, d):
    # partitions array into subarrays grouped by unique value
    outputPartition = []
    total = 0
    dim = inputArray[:, d]
    for val in np.unique(dim):
        datacount = len(np.where(dim == val )[0])
        outputPartition.append(inputArray[total:total+datacount])
        total += datacount
    return np.array(outputPartition)

def BUC(inputArray, curdim, maxdim, intmap, dimmap, min_sup, outputRec=""):
    #if dim == 3: return outputRec
    for d in range(curdim, maxdim):
        print(inputArray)
        print(inputArray.shape)
        C = len(np.unique(inputArray[:,d]))  # cardinality
        print(C)
        inputArray = partition(inputArray, d)
        k = 0
        for i in inputArray:  # for each partition
            #c = len(i)  # datacount
            c = len(i[:,4])
            if c >= min_sup:
                #outputRec[:, d] = i[k:, d]
                outputRec += aggregate(i, [d], intmap, dimmap, min_sup)
                return (outputRec + BUC(i[k:k+c-1], d+1, 3, intmap, dimmap, min_sup, outputRec))
            k += c
        #outputRec[:, d] = all
    return outputRec


print("(Item)")
outputRec = BUC(inputArray, 0, 3, intmap, dimmap, min_sup)
print(outputRec)

print("(Item)(Location)")
outputRec = BUC(inputArray, 1, 3, intmap, dimmap, min_sup, outputRec)
print(outputRec)

