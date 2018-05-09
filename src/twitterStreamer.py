'''
Created on Jun 5, 2017

@author: lbozarth
'''
from functools import partial
import random,itertools, csv
from time import sleep
import tweepy  # https://github.com/tweepy/tweepy

import multiprocessing as mp
import numpy as np
import pandas as pd
from lbtools import twitterAPICalls
from lbtools import ioTools
import os

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def getAPI(row):
    #     print(row)
    consumer_key = row[0]
    consumer_secret = row[1]
    access_token = row[2]
    access_token_secret= row[3]
#    print("credits", consumer_key, consumer_secret, access_token, access_token_secret)
#    print(row[:10])

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def run_single_tweets(row):
    api = getAPI(row)
    tweetids = row[4:]
    tidlst = chunkIt(tweetids, 300)
    i = 1

    wdir =  "../data/twitter/"
    for tids in tidlst:
        print("length of tids is", len(tids))
        try:
            wfn = os.path.join(wdir, tids[0]+".txt")
            if os.path.exists(wfn):
                continue
            tweets = twitterAPICalls.get_tweets_byId(api, tids)
            if tweets is None or len(tweets)==0:
                continue
            if isinstance(tweets, dict):
                print(tweets)
                continue

            with open(wfn, 'w') as f:
                f.write('\n'.join(tweets))
            i -= 1
            if i < 0:
                break
        except Exception as e:
            print(e)
    return

def getTweetIds():
    lines = ioTools.readFile_byLine("../data_open/archivedData.csv")
    print('number of tweet ids', len(lines))
    return lines

def runTweets():
    fn = "../data/credits.txt"
    rows = ioTools.readFile(fn, ",")
    rows = rows[1:]
    tweetids = getTweetIds()
    # random.shuffle(tweetids)
    chunks = chunkIt(tweetids, len(rows))
    res = []
    for i in range(len(rows)):
        res.append(rows[i] + chunks[i])
    p = mp.Pool(len(rows))
    ndfs = p.map(run_single_tweets, res)
#     ndfs = list(itertools.chain(*ndfs))
#     df = pd.DataFrame(ndfs)
#     print(df.head(2))
#     print(len(df.index))
#     wfn = "../data/twitter/candidate_tweets.csv"
#     df.to_csv(wfn, sep='\t', header=True, index=False)

def start():
    runTweets()

if __name__ == '__main__':
    start()
    pass
