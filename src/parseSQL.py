import requests, os, io, glob
import numpy as np
import pandas as pd
import pprint, json
import ast
from pymongo import MongoClient
from bson.son import SON
from lbtools.nlpPreprocessor import NLPPrep
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from lbtools import spaCyProcessor
from lbtools import ioTools
from sklearn.feature_extraction.text import CountVectorizer


def main():
    with open("../data/adexp04132016_twitterdataduplicate.sql") as f:
        dat = f.read()
        dats = dat.split("('")
        print(len(dats))
        resss = []
        for row in dats:
            try:
                tid = np.int64(row.split("',")[0])
                # print(tid)
                if len(str(tid)) < 12: #tid is 15 digits
                    continue
                # print(row)
                resss.append(tid)
                # break
            except ValueError as e:
                continue

        print(len(resss))
        ioTools.writeToFile_writeRows_wrapper("../data/archivedData.csv", ',', resss)
    return


main()