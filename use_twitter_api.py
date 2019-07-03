# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:47:41 2019

@author: Swooty
"""
from requests_oauthlib import OAuth1
import requests
import json
import pickle

filename = 'Twitter_API_keys'
with open(filename, 'r') as f:
        keydict = json.load(f)

# create an auth object
auth = OAuth1(
    keydict['api_key'],
    keydict['api_secret_key'],
    keydict['access_token'],
    keydict['access_token_secret']
)


url = 'https://api.twitter.com/1.1/tweets/search/30day/development.json'

def query_twitter(param_dict):
    response = requests.get(
        url,
        auth=auth,
        params=param_dict
    )
    return response.json()

try:
    with open(r'usable_tweets', 'rb') as f: 
        usable_tweets = pickle.load(f)
except('FileNotFoundError'):
    usable_tweets = []
    
try: 
    with open(r'current_query_status', 'rb') as f:
        current_query_dict = pickle.load(f)
        i = current_query_dict['i']
        param_dict = current_query_dict['param_dict']
        more_pages = current_query_dict['more_pages']
except('FileNotFoundError'):
    more_pages = True
    param_dict = {'query' : 'subscription service lang:en'}
    i=0
    
while more_pages:
    response = query_twitter(param_dict)

    try:
        for tweet_dict in response['results']:
            if tweet_dict['retweet_count']+tweet_dict['favorite_count']>0:
                if len(tweet_dict['entities']['hashtags']) >0 :
                    usable_tweets.append(tweet_dict)
    except(KeyError):
        print(response['error']['message'])
        print('Pickling up what we got')
        with open(r'usable_tweets', 'wb') as f: 
            pickle.dump(usable_tweets,f)
        with open(r'current_query_status', 'wb') as f:
            pickle.dump({'i':i,
                         'param_dict':param_dict,
                         'more_pages':more_pages},f)
            
    try:
        next_query = response['next']
        param_dict['next'] = next_query
    except(KeyError):
        if 'error' in response.keys():
            print(response['error']['message'])
        more_pages = False
    print('page {i}'.format(i=i))
    i +=1
