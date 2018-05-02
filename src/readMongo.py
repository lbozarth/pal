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

def genCleanText(x):
    x = x.lower().strip()
    # print('before', x[:100])
    x = NLPPrep(x).cleanTweet().removePunc().tokenizeToLst().lemma_lst().removeStopwords_lst().get_lst_doc()
    # print("after", x[:100])
    return x

def removeStop(x):
    x = NLPPrep(x).tokenizeToLst().removeStopwords_lst().get_lst_doc()
    return x

def genCleanText_nouns(x):
    x = x.lower().strip()
    # print('before', x[:100])
    x = NLPPrep(x).cleanTweet().removePunc().get_doc_mod()
    x = spaCyProcessor.get_POS_map(x, ['NOUN', 'PROPN'])
    return " ".join(x)

def genWordCloud_party(x):
    wordcloud = WordCloud().generate(x['tweet_text'])
    wds = wordcloud.words_
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # wfn = "../data/plots/wordCloud/party/%s_wc.png" % x['party']
    # print(wfn)
    # plt.savefig(wfn)
    sorted(wds.items(), key=lambda x: -x[1])
    ks = list(wds.keys())
    return ", ".join(ks)

def genWordCloud_agent(x):
    wordcloud = WordCloud().generate(x['tweet_text'])
    wds = wordcloud.words_
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # wfn = "../data/plots/wordCloud/agent/%s_wc.png" % x['userhandle']
    # print(wfn)
    # plt.savefig(wfn)
    sorted(wds.items(), key=lambda x: -x[1])
    ks = list(wds.keys())
    return ", ".join(ks)

def aggStr(x):
    return " ".join(x)

def genWordcloud(db):
    # df = pd.read_csv("../data/pal_tweets.csv", sep="\t", header=0)
    # df = df[[" UserHandle", 'Party', "h", 'Language']]
    # df.columns = ['userhandle', 'party', 'tweet_text', 'lang']
    # df = df[df['lang']=="English"].reset_index()
    #
    # df = df.groupby(['userhandle','party'], as_index=False).agg({"tweet_text":aggStr})
    # df.reset_index(inplace=True, drop=True)
    # print(df.head(2))
    # print(len(df.index))
    # df['tweet_text'] = df['tweet_text'].apply(genCleanText_nouns)
    # df.to_csv("../data/pal_tweets_clean_nouns.csv", sep="\t", header=True, index=False)
    # print(df.head(2))

    df = pd.read_csv("../data/pal_tweets_clean_nouns.csv", sep="\t", header=0)
    df['tweet_text'] = df['tweet_text'].apply(removeStop)
    print(df.head(2))
    df['tokens'] = df.apply(genWordCloud_agent, axis=1)
    print(df.head(2))

    dfs = df[['userhandle', 'tokens']]
    wfn = "../data/wordCloud_byAgent_200c.csv"
    dfs.to_csv(wfn, sep="\t", header=True, index=False)

    df1 = df.groupby('party', as_index=False).agg({"tweet_text": aggStr})
    df1['tokens'] = df1.apply(genWordCloud_party, axis=1)

    dfs = df1[['party', 'tokens']]
    wfn = "../data/wordCloud_byParty_200c.csv"
    dfs.to_csv(wfn, sep="\t", header=True, index=False)
    print(df1.head(2))

    return

def genPhrases(db):
    # df = pd.read_csv("../data/pal_tweets.csv", sep="\t", header=0)
    # df = df[[" UserHandle", 'Party', "h", 'Language']]
    # df.columns = ['userhandle', 'party', 'tweet_text', 'lang']
    # df = df[df['lang']=="English"].reset_index()
    # df['tweet_text'] = df['tweet_text'].apply(genCleanText)
    # print(df.head(2))
    #
    # df.to_csv("../data/pal_tweets_clean.csv", sep="\t", header=True, index=False)

    df = pd.read_csv("../data/pal_tweets_clean.csv", sep="\t", header=0)
    unique_parties = df['party'].unique().tolist()
    for p in unique_parties:
        print('party is ', p)
        dfc = df[df['party']==p]
        dfc = dfc[dfc['tweet_text'].str.len()>10]
        tweets = dfc['tweet_text'].tolist()
        print(tweets[:2])
        try:
            cv = CountVectorizer(ngram_range=(3, 6), min_df=25)
            cv_fit = cv.fit_transform(tweets)
            voc = cv.vocabulary_

            counts = cv_fit.toarray().sum(axis=0)
            resss = []
            for k, v in voc.items():
                resss.append([k, counts[v]])

            dff = pd.DataFrame(resss, columns=['phrase', 'total_count'])
            dff['num_tokens'] = dff['phrase'].apply(lambda x: len(x.split(" ")))
            dff.sort_values(['num_tokens', 'total_count'], ascending=False, inplace=True)
            dff = dff[['phrase', 'num_tokens', 'total_count']]
            wfn = "../data/phrases/party/%s_25c.csv" % p
            dff.to_csv(wfn, sep="\t", header=True, index=False)
        except ValueError as e:
            print(e)
            continue


def genHashtagNetwork(db):
    pip = [{"$match": {"hashtags":{"$ne":None}}},
           {"$unwind": "$hashtags"},
           {"$group": {"_id": {"agents_id":"$agents_id", "hashtag":"$hashtags"}, "count":{"$sum":1}}}]

    result = db.tweets.aggregate(pip)
    resss = []

    for r in result:
        resss.append([r['_id']['agents_id'], r['_id']['hashtag'], r['count']])
    df = pd.DataFrame(resss, columns=['agent', 'hashtag', 'count'])

    dfa = pd.read_csv("../data/agents_all.csv", header=0, sep="\t")
    df = pd.merge(df, dfa, left_on='agent', right_on='_id').reset_index(drop=True)

    # # hashtags by party
    # dfh = df.groupby(['hashtag','party'], as_index=False)['count'].sum()
    # dfh.reset_index(drop=True, inplace=True)
    # print(dfh.head(2))
    # dfh.columns = ['hashtag', 'party','total_count']
    # dfh.set_index(['party','hashtag']).groupby(level=['party','hashtag'])['total_count'].nlargest(25).reset_index()
    # print(dfh.head(2))
    # dfh.sort_values(by=['party','total_count'], ascending=False, inplace=True)
    # dfh = dfh[['party', 'hashtag', 'total_count']]
    # dfh.to_csv("../data/hashtags_byFreqAndParty.csv", sep="\t", header=True, index=False)
    #
    # # unique hashtags
    # dfh = df.groupby('hashtag', as_index=False)['count'].sum()
    # dfh.reset_index(drop=True, inplace=True)
    # # print(dfh.head(2))
    # dfh.columns = ['hashtag', 'total_count']
    # dfh = dfh[dfh['total_count'] >= 100]
    # dfh.sort_values(by='total_count', ascending=False, inplace=True)
    # dfh.to_csv("../data/hashtags_byFreq.csv", sep="\t", header=True, index=False)

    dfh = pd.read_csv("../data/fixed_hashtags.csv", sep="\t", header=0)

    # subset
    df1 = df[['agent', 'hashtag', 'count', 'party']]
    df1['hashtag'] = df1['hashtag'].str.lower().str.strip()
    print(len(df1.index))
    df1 = df1[df1['hashtag'].isin(dfh['hashtag'])]
    df1.reset_index(drop=True, inplace=True)
    print(len(df1.index))
    df1.columns = ['Source', 'Target', 'weight', 'src_party']
    wfn = "../data/hashtags_fixed.csv"
    df1.to_csv(wfn, sep="\t", header=True, index=False)


# Generate agent ==> retweetee relationship where agent retweeted retweetee x times
def genRetweetNetwork(db):
    pip = [{"$match": {"retweet":{"$ne":None}}},
           {"$group": {"_id": {"agents_id":"$agents_id", "retweet":"$retweet"}, "count":{"$sum":1}}}]
    # pip = [{"$match":{"agents_id":"AAPInNews"}}]
    result = db.tweets.aggregate(pip)
    resss = []
    for r in result:
        resss.append([r['_id']['agents_id'], r['_id']['retweet'], r['count']])
    df = pd.DataFrame(resss, columns=['agent', 'retweet', 'count'])

    dfa = pd.read_csv("../data/agents_all.csv", header=0, sep="\t")
    df = pd.merge(df, dfa, left_on='agent', right_on='_id').reset_index(drop=True)
    print(df.head(2))

    dfa2 = dfa.rename(columns=lambda x: 'retweet_' + x)
    df = pd.merge(df, dfa2, left_on='retweet', right_on='retweet__id').reset_index(drop=True)
    print(df.head(2))

    # subset
    df = df[['agent', 'retweet', 'count', 'party', 'retweet_party']]
    df.columns = ['Source', 'Target', 'weight', 'src_party', 'tgt_party']
    wfn = "../data/retweets.csv"
    df.to_csv(wfn, sep="\t", header=True, index=False)
    return

# Generate agent ==> mentionee relationship where agent mentioned mentionee x times
def genMentionNetwork(db):
    pip = [{"$match": {"mentions":{"$ne":None}}},
           {"$unwind": "$mentions"},
           {"$group": {"_id": {"agents_id":"$agents_id", "mention":"$mentions"}, "count":{"$sum":1}}}]

    result = db.tweets.aggregate(pip)
    resss = []

    for r in result:
        resss.append([r['_id']['agents_id'], r['_id']['mention'], r['count']])
    df = pd.DataFrame(resss, columns=['agent', 'mention', 'count'])

    dfa = pd.read_csv("../data/agents_all.csv", header=0, sep="\t")
    df = pd.merge(df, dfa, left_on='agent', right_on='_id').reset_index(drop=True)

    dfa2 = dfa.rename(columns=lambda x: 'mention_' + x)
    df = pd.merge(df, dfa2, left_on='mention', right_on='mention__id').reset_index(drop=True)
    print(df.head(2))
    print(len(df.index))

    # subset
    df = df[['agent', 'mention', 'count', 'party', 'mention_party']]
    df.columns = ['Source', 'Target', 'weight', 'src_party', 'tgt_party']
    wfn = "../data/mentions.csv"
    df.to_csv(wfn, sep="\t", header=True, index=False)
    return

def genAgentNodeTable():
    dfa = pd.read_csv("../data/agents_all.csv", header=0, sep="\t")
    dfa1 = dfa[['_id', 'party']]
    dfa1.columns = ['ID', 'party']
    dfa1['Label'] = dfa1['ID']
    dfa1.to_csv("../data/nodeTable.csv", header=True, index=False)
    return

def genAgentNodeTable_withHashtags():
    dfa = pd.read_csv("../data/agents_all.csv", header=0, sep="\t")
    dfa1 = dfa[['_id', 'party']]
    dfa1.columns = ['ID', 'party']
    dfa1['Label'] = dfa1['ID']
    dfa1['type'] = 'party'
    dfa1 = dfa1[['ID', 'Label', 'party', 'type']]

    dfa2 = pd.read_csv("../data/fixed_hashtags.csv", header=0, sep="\t")
    dfa2.columns = ['ID', 'weight', 'party']
    dfa2['Label'] = dfa2['ID']
    dfa2['type'] = 'hashtag'
    dfa2 = dfa2[['ID', 'Label', 'party', 'type']]

    df_full = pd.concat([dfa1, dfa2], axis=0)
    df_full['party'] = df_full['party'].apply(lambda x: "unlabeled" if type(x)==float else x)
    print(df_full.head(2))
    df_full.to_csv("../data/nodeTable_withHashtags_fixed.csv", header=True, index=False)
    return

def cleanHashtags():
    df = pd.read_csv("../data/hashtags_byFreq.csv", sep="\t", header=0)
    df['hashtag'] = df['hashtag'].str.lower()
    df = df.groupby('hashtag', as_index=False)['total_count'].sum()
    df.sort_values(['hashtag'], inplace=True)
    print(df.head(2))
    df=df[df['hashtag'].str.len()>=3]
    df.to_csv("../data/hashtags_byFreq_clean.csv", sep="\t", header=True, index=False)
    return


def fixFile():
    df = pd.read_csv("../data/hashtags_byFreq_clean.csv", sep="\t", header=0)
    resss = []
    firstLine = True
    for line in ioTools.readFile_byLine("../data/brokenFile.csv"):
        if firstLine:
            firstLine = False
            continue
        else:
            if line[-1].isdigit():
                resss.append(np.nan)
                continue
            for idx in range(len(line)-1):
                idx +=1
                if line[-idx].isdigit():
                    resss.append(line[-idx+1:])
                    break

    print(resss)
    print(len(resss))
    df_fix = pd.DataFrame(resss, columns=['label'])
    df = pd.concat([df, df_fix], axis=1)
    print(df)

    df.to_csv("../data/fixed_hashtags.csv", sep=",", header=True, index=False)


def main():
    client = MongoClient('localhost', 27017)
    db = client.pal # use database
    # genRetweetNetwork(db)
    # genMentionNetwork(db)
    # genHashtagNetwork(db)
    # genAgentNodeTable()
    genAgentNodeTable_withHashtags()
    # genWordcloud(db)
    # genPhrases(db)
    # cleanHashtags()
    # fixFile()
    return

main()