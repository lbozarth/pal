'''
Created on Jun 5, 2017

@author: lbozarth
'''
import csv, os, tweepy, json, sys
from time import sleep
from tweepy.error import TweepError

def get_tweets(api, screen_id):
    try:
        user_timeline = []
        for p in tweepy.Cursor(api.user_timeline, id=screen_id, count=200).pages():
            user_timeline.extend(p)
        user_timeline = [obj._json for obj in user_timeline]
        return user_timeline
    except TweepError as e:
        if e.api_code is not None and e.api_code != 88:
            return {"error": str(e.api_code)}
        return {"error":e.response}

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_tweets_byId(api, tweetids):
    try:
        tweets = []
        tidlst = chunks(tweetids, 100)
        for tids in tidlst:
            t100 = api.statuses_lookup(tids)
            t100 = [json.dumps(obj._json, ensure_ascii=False) for obj in t100]
            t100 = [obj.replace("\n", "").replace("\r", "").replace("\t", "") for obj in t100]
            tweets.extend(t100)
        return tweets
    except TweepError as e:
        if e.api_code is not None and e.api_code != 88:
            return {"error": str(e.api_code)}
        return {"error":e.response}

def get_recent_timeline(api, screen_id):
    try:
        user_timeline = api.user_timeline(id=screen_id, count=200, include_entities=True)
        user_timeline = [obj._json for obj in user_timeline]
        return user_timeline
    except TweepError as e:
        print(str(e))
        if e.api_code is not None and e.api_code != 88:
            return {"error": str(e.api_code)}
        return {"error":e.response}

def get_user_profile(api, screen_id):
    try:
        up = api.get_user(id=screen_id)
#         user_profile = json.load(up)
#         print(user_profile)
#         user_profile = { key : str(value) for key,value in json.loads(up)}
#         user_profile = [up.id, up.screen_name, up.name, up.description, up.statuses_count, up.friends_count, up.followers_count, up.url, up.created_at, up.location, up.geo_enabled]
        return up
    except TweepError as e:
        print(str(e))
        if e.api_code is not None and e.api_code != 88:
            return {"error": str(e.api_code)}
        return {"error":e.response}

def get_all_friends_ids_largedata(api, screen_id):
    allFriends = []
    friendCursor = tweepy.Cursor(api.friends_ids, id=screen_id, count=5000).pages()
    while True:
        try:
            block = friendCursor.next()
            if(isinstance(block, list)):
                allFriends.extend(block)
            else:
                allFriends.append(block)
        except StopIteration as e:
            print("friends iteration completed")
            break;
        except tweepy.error.TweepError as e:
            print(str(e))
            if e.api_code is not None and e.api_code != 88:
                return {"error": str(e.api_code)}
            return {"error":e.response}  
    return allFriends


def get_all_friends_ids(api, screen_id):
    allFriends = []
    while True:
        try:
            for block in tweepy.Cursor(api.friends_ids, id=screen_id, count=5000).pages():
                if(isinstance(block, list)):
                    allFriends.extend(block)
                else:
                    allFriends.append(block)
            break
        except tweepy.error.TweepError as e:
            print(str(e))
            if e.api_code is not None and e.api_code != 88:
                return {"error": str(e.api_code)}
            return {"error":e.response}
    return allFriends

def get_all_followers_ids(api, screen_id):
    allFollowers = []
    while True:
        try:
            for block in tweepy.Cursor(api.followers_ids, id=screen_id, count=5000).pages():
                if(isinstance(block, list)):
                    allFollowers.extend(block)
                else:
                    allFollowers.append(block)
            break
        except tweepy.error.TweepError as e:
            print(str(e))
            if e.api_code is not None and e.api_code != 88:
                return {"error": str(e.api_code)}
            return {"error":e.response}
    return allFollowers

def get_all_followers_ids_largedata(api, screen_id):
    allFollowers = []
    followerCursor = tweepy.Cursor(api.followers_ids, id=screen_id, count=5000).pages();
    while True:
        try:
            block = followerCursor.next()
            if(isinstance(block, list)):
                allFollowers.extend(block)
            else:
                allFollowers.append(block)
        except StopIteration as e:
            print("follower iteration completed")
            break;
        except tweepy.error.TweepError as e:
            print(str(e))
            if e.api_code is not None and e.api_code != 88:
                return {"error": str(e.api_code)}
            return {"error":e.response}
    return allFollowers

if __name__ == '__main__':
    pass