'''
Created on Apr 5, 2017

@author: lbozarth
'''
import math, csv, os
import numpy as np
import pandas as pd


def deleteFiles(fns):
    for fn in fns:
        deleteFile(fn)

def deleteFile(fn):
    if os.path.exists(fn):
        os.remove(fn)

def writeToFile_dump(filename, load):
    with open(filename, "w") as f:
        f.write(load)
    return

def writeToFile_writeRows(filename, delim, rows):
    with open(filename, "w") as f:
        writer = csv.writer(f, delimiter=delim, lineterminator="\n")
        writer.writerows(rows)  
    return

def writeToFile_writeRows_wrapper(filename, delim, rows):
    res = []
    for row in rows:
        res.append([row])
    with open(filename, "w") as f:
        writer = csv.writer(f, delimiter=delim, lineterminator="\n")
        writer.writerows(res)  
    return

def appendToFile_writeRows(filename, delim, rows):
    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter=delim, lineterminator="\n")
        writer.writerows(rows)  
    return


def appendToFile_writeRow(filename, delim, row):
    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter=delim, lineterminator="\n")
        writer.writerow(row)  
    return

def readFile(filename, delim):
    data = []
    with open(filename, "rU") as f:
        reader = csv.reader(f, delimiter=delim, lineterminator="\n", dialect=csv.excel_tab)
        for row in reader:
            data.append(row)
    return data

def readFile_byLine(filename):
    data = []
    with open(filename, "r") as f:
        data = f.readlines();
        data = [x.strip() for x in data] 
    return data
def readFile_dump(filename):
    with open(filename, "r") as f:
        return f.read()

if __name__ == '__main__':
    pass