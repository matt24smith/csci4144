#!/usr/bin/env python3
# coding: utf-8

import numpy as np 
import csv

def cubeslice(datacube, cubeix, prevsets):  # chainable!
    nextsets = []
    for s in prevsets:
        for value in np.unique(datacube[cubeix]):
            nextsets += [s[np.where(datacube[cubeix][s] == value)[0]]]
    return np.array(nextsets)

def printaggregations(csvcolumns, subsets, slices, datacube):
    def p_cols(csvcolumns, slices, prefix="  "):
        print(end=prefix)
        for ix in slices: print(csvcolumns[ix], end=" ")
        print()

    def p_agg(s, slices, datacube, prefix="    "):
        if len(s) == 0: return
        for attr in slices: prefix += (datacube[attr][s][0] + ' ')
        spaces = " " * (40 - len(prefix))
        print(f'{prefix}:{spaces}{sum(datacube[5].astype(int)[s])}')

    if sum(slices) == 7 or sum(slices) == 10:  # convert table to (n-1)D tables
        slices = slices[1:]
        print("Canada")
        p_cols(csvcolumns, slices)
        for s in subsets[0:int(len(subsets)/2)]:
            p_agg(s, slices, datacube)
        print("\nUnited States")
        p_cols(csvcolumns, slices)
        for s in subsets[int(len(subsets)/2):len(subsets)]:
            p_agg(s, slices, datacube)
    else:
        p_cols(csvcolumns, slices, "")
        for s in subsets:
            p_agg(s, slices, datacube, "")
    print()

def inputoperation():
    opvals = ["1. ()", 
              "2. (Country)", 
              "3. (Time_Year)", 
              "4. (Time_Quarter - Time_Year)", 
              "5. (Car_Manufacturer)",
              "6. (Country, Time_Year)", 
              "7. (Country, Time_Quarter - Time_Year)",
              "8. (Country, Car_Manufacturer)", 
              "9. (Time_Year, Car_Manufacturer)",
              "10.(Time_Quarter - Time_Year, Car_Manufacturer)",
              "11.(Country, Time_Year, Car_Manufacturer)",
              "12.(Country, Time_Quarter - Time_Year, Car_Manufacturer)"]
    print("Valid operations:")
    for op in opvals:
        print("   " + op )
    olap = input("Select an OLAP Operation (1-12): ")
    try:
        assert(int(olap) >= 1 and int(olap) <= 12)
        return opvals[int(olap) - 1]
    except:
        print("\nInvalid operation!")
        return inputoperation()

def readdata(filename):
    recordId = np.array([], dtype=int)
    country = np.array([])
    year = np.array([], dtype=int)
    quarter = np.array([], dtype=int)
    brand = np.array([])
    sales = np.array([], dtype=int)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                csvcolumns = row
                line_count += 1
            else:
                recordId = np.append(recordId, int(row[0])-1)
                country = np.append(country, row[1])
                year = np.append(year, int(row[2]))
                quarter = np.append(quarter,int(row[3]))
                brand = np.append(brand, row[4])
                sales = np.append(sales, int(row[5]))
                line_count += 1
    return (np.array([recordId, country, year, quarter, brand, sales]), 
            csvcolumns)

def writedata(filename, datacube, csvcolums):
    with open(filename, "w") as f:
        for c in csvcolumns:
            f.write(c)
            if c != 'Sales_Units': f.write(",")
            else : f.write("\n")
        for x in range (0, 100):
            f.write(f'{x+1},{datacube[1][x]},{datacube[2][x]},'+
                    f'{datacube[3][x]},{datacube[4][x]},{datacube[5][x]}\n' )

# sort the data for country, year, quarter
datacube, csvcolumns = readdata('Car_Sales_Data_Set.csv')
subsets = np.array([range(0, len(datacube[0]))])
for ix in [1, 2, 3]: subsets = cubeslice(datacube, ix, subsets)
sortix = np.hstack(subsets)
datacube = np.array([x[sortix] for x in datacube])
writedata("Car_Sales_Data_Set_Sorted.csv", datacube, csvcolumns)

# parse user input
olap = inputoperation()

slices = np.array([]).astype(int)

if "Country" in olap:         
   slices = np.append(slices, 1)
if "Year" in olap:            
   slices = np.append(slices, 2)
if "Quarter" in olap:         
   slices = np.append(slices, 3)
if "Manufacturer" in olap:    
   slices = np.append(slices, 4)
slices

# perform operations on data cube
subsets = np.array([range(0, len(datacube[0]))])
for sliceix in slices:
    subsets = cubeslice(datacube, sliceix, subsets)

# print the results
printaggregations(csvcolumns, subsets, slices, datacube)

