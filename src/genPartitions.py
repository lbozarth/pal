import requests, os, io, glob
import numpy as np
import pandas as pd
import pprint, json
import ast
import dateutil.parser as parser
from datetime import datetime
import time,re
from ttp import ttp
from collections import OrderedDict
from lbtools.nlpPreprocessor import NLPPrep
from lbtools import spaCyProcessor
from sklearn.feature_extraction.text import CountVectorizer

import preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.URL, p.OPT.RESERVED)

tweetParser = ttp.Parser()
def getRetweet(x):
    try:
        r = re.findall(r'^(RT|rt)( @\w*)?', str(x))
        if r:
            rt = r[0][1].replace(":", "").replace("@", "")
            return rt.strip()
        return np.nan
    except TypeError as e:
        print('tweet_text is', x)
        return np.nan

def getMention(x):
    mentions = re.findall(r'(?<!RT\s)@\S+', str(x))
    if len(mentions)>0:
        mentions = [x.replace("@", "").replace(":", "").strip() for x in mentions]
        return mentions
    return np.nan

def getHashtags(x):
    result=tweetParser.parse(str(x))
    # print(result.reply)
    # print(result.html)
    # print(result.tags)
    if (len(result.tags)>0):
        return result.tags
    return np.nan

def getUrls(x):
    result = tweetParser.parse(str(x))
    if (len(result.urls)>0):
        return result.urls
    return np.nan

def readDF_tweets():
    df = pd.read_csv("../data/pal_tweets.csv", sep="\t", header=0)
    df_tweets = df[['TweetID', " UserHandle", ' TweetDate','h', ' RetweetCount', ' FavoriteCount', 'Message Type', 'Language', 'Vernacular']]
    df_tweets.columns = ['_id', 'agents_id', 'tweet_date', 'tweet_text', 'retweet_count', 'fav_count','message_type', 'lang', 'vernacular']
    df_tweets['posix_time'] = df_tweets['tweet_date'].apply(lambda x: time.mktime(datetime.strptime(x, "%m/%d/%Y").timetuple()))
    df_tweets['retweet'] = df_tweets['tweet_text'].apply(getRetweet)
    df_tweets['mentions'] = df_tweets['tweet_text'].apply(getMention)
    df_tweets['hashtags'] = df_tweets['tweet_text'].apply(getHashtags)
    df_tweets['urls'] = df_tweets['tweet_text'].apply(getUrls)

    # print(df_tweets.head(2))
    # jsonresult = df_tweets.to_json(orient='records')
    # rows = json.loads(jsonresult)
    # new_rows = [OrderedDict([
    #         (key, row[key]) for key in df_tweets.columns
    #         if (key in row) and (row[key] != np.nan)
    #     ])
    #     for row in rows
    # ]
    #
    # new_json_output = json.dumps(new_rows)
    # print(new_json_output)

    df_tweets.to_json('../data/tweets_all.json', orient='records', lines=True, force_ascii=False)
    return

def readDF_agents():
    df = pd.read_csv("../data/pal_tweets.csv", sep="\t", header=0)
    df_agent = df[[" UserHandle", 'Type', 'State', 'Party', 'Party Type', 'Politician Type', 'South']]
    df_agent.columns = ['_id', 'agent_type', 'state', 'party', 'party_type', 'politician_type', 'south']
    # df_agent = df[[" UserHandle", ' RetweetCount', ' FavoriteCount', 'Type', 'State', 'Party', 'Party Type', 'Politician Type', 'South']]
    # df_agent.columns = ['_id', 'retweet_count', 'fav_count', 'agent_type', 'state', 'party', 'party_type', 'politician_type', 'south']
    df_agent.drop_duplicates('_id', keep='first', inplace=True)
    df_agent.reset_index(drop=True)
    print(df_agent.head(2))

    df_agent.to_json('../data/agents_all.json', orient='records', lines=True)
    df_agent.to_csv("../data/agents_all.csv", sep="\t", header=True, index=False)

    # df_agent['json'] = df_agent.apply(convertToJson, axis=1)
    # wfn = "../data/agents_all.json"
    # df_agent['json'].to_csv(wfn, sep="\t", header=False, index=False)

def test():
    dx = "9/19/2017"
    date = parser.parse(dx)
    print(date.isoformat())

    tweet = 'RT @one: @two: @three #teuh #oeun ####he###oe oeu  https://t.co/jZzUp08Cgk	explain. You can also use spacy.explain() to get the description for the string representation of a tag. For example, spacy.explain("RB") will return "adverb".'
    r = re.findall(r'^(RT|rt)( @\w*)?', tweet)
    print('r2',r[0][1])
    result=tweetParser.parse(tweet)
    # print(result.reply)
    print(result.urls)
    print(result.tags)

    clean_t = p.clean(tweet)
    print(clean_t)

    nlp = NLPPrep(tweet)
    clean_t2 = nlp.cleanTweet().removePunc().get_doc_mod()
    print(clean_t2)

    res = spaCyProcessor.get_POS_map(clean_t2, ['NOUN', 'PROPN'])
    print("nouns are ", res)

def test2():
    texts = ["dog cat fish", "dog cat cat", "fish bird", 'bird', 'cat cat', 'dog cat']
    cv = CountVectorizer(ngram_range=(1,3), min_df=2)
    cv_fit = cv.fit_transform(texts)
    voc = cv.vocabulary_

    counts = cv_fit.toarray().sum(axis=0)
    resss = {}
    for k,v in voc.items():
        resss[k] = counts[v]

    print(resss)
    return

def main():
    test()
    test2()
    # readDF_agents()
    # readDF_tweets()
    pass

main()