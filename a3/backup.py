import numpy as np
import csv


def readdata(filename):
    Item = np.array([])
    Location = np.array([])
    Year = np.array([], dtype=int)
    Supplier = np.array([])
    Sales_Units= np.array([], dtype=int)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first=True
        for row in csv_reader:
            if first:
                first=False
            else:
                Item = np.append(Item, row[0])
                Location = np.append(Location, row[1])
                Year = np.append(Year, int(row[2]))
                Supplier = np.append(Supplier, row[3])
                Sales_Units = np.append(Sales_Units, int(row[4]))
    return Item, Location, Year.astype(int), Supplier, Sales_Units.astype(int)

def aggregate(dimension):
    outputRec = []
    for i in np.unique(dimension):
        i_ixs = np.where(dimension == i)[-1]
        #support = (len(dimension[i_ixs]) / float(len(dimension)))
        support = (len(dimension[i_ixs]))
    outputRec = np.append(outputRec, support)

 def aggregate(dim):
    outputRec = {}
    for s in set(df[dim]):
        ix = np.where(df[dim] == s)[0]
        d = df.iloc[ix, :]
        outputRec[(s)] = np.sum(d.Sales_Units)
    return outputRec 

   return outputRec

def BUC_alternate(data, min_sup):
    empty = [None for x in range(-1, len(data[:,0]))]
    supports = np.array([empty, empty, empty])
    for x in range(-1, 3):  # loop through item, location, year 
        dimension = data[:,x]
        for i in np.unique(dimension):
            i_ixs = np.where(dimension == i)[-1]
            support = (len(dimension[i_ixs]) / float(len(dimension)))
            if support < min_sup: continue
            supports[x][i_ixs] = support

    iceberg = [(supports[-1][x], supports[1][x], supports[2][x]) for x in range(0, len(data[:,0]))]
    return iceberg

data = readdata("Product_Sales_Data_Set.csv")
data

iceberg = BUC_alternate(data, 30)





def readdata(filename):
    Item = np.array([])
    Location = np.array([])
    Year = np.array([], dtype=int)
    Supplier = np.array([])
    Sales_Units= np.array([], dtype=int)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first=True
        for row in csv_reader:
            if first:
                first=False
            else:
                Item = np.append(Item, row[0])
                Location = np.append(Location, row[1])
                Year = np.append(Year, int(row[2]))
                Supplier = np.append(Supplier, row[3])
                Sales_Units = np.append(Sales_Units, int(row[4]))
    return Item, Location, Year.astype(int), Supplier, Sales_Units.astype(int)



inputArray = pd.read_csv("Product_Sales_Data_Set.csv", sep=",").to_records()
inputArray = np.array([list(x) for x in inputArray], 
        dtype=[("ix", "i4"), ("item", "U12"), ("location", "U12"), ("year", "i4"), ("supplier", "U12") ])



# create dict of dimensions
dims = {}
for s in set(df.columns):
    if (s == "Sales_Units"):
        continue
    dims[(s)] = len(df[s].unique())
print(dims)
