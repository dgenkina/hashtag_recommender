# -*- coding: utf-8 -*-
"""
Created on Sun May 19 12:09:22 2019

@author: swooty
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy import sparse
from scipy.sparse import dok_matrix, coo_matrix
#import progressbar
import re
pattern = re.compile('[\W_]+')

df = pd.read_csv('dashboard_x_usa_x_filter_nativeretweets.csv', encoding='iso-8859-1')
df = df[df['Favs']+df['RTs']>0]

tweets = df['Tweet content']
hashtags = []
for tweet in tweets:
   # tweet = tweet.decode('iso-8859-1')
    hashtags_local = set()
    for tweet_word in tweet.split():
        if tweet_word.startswith("#"):
            tweet_word = pattern.sub('', tweet_word) 
            hashtags_local.add(tweet_word)
    hashtags.append(hashtags_local)
df['hashtags'] = hashtags

df_eng = df.loc[df['Tweet language (ISO 639-1)']=='en']
hashtags = df_eng['hashtags'].tolist()

all_hashtags = set().union(*hashtags)
all_hashtags_list = list(all_hashtags)


index_list = []
for hashtag_set in hashtags: #progressbar.progressbar(hashtags):
    local_list = []
    for ind, tag in enumerate(hashtag_set):
        ind = all_hashtags_list.index(tag)
        local_list.append(ind)
    index_list.append(local_list)

df_eng['hashtag_indexes'] = index_list
df_eng['scaled_favs'] = df_eng['Favs']/df_eng['Followers']
df_eng['scaled_rts'] = df_eng['RTs']/df_eng['Followers']
df_eng.to_csv('eng_tweets_short.csv')

num = 0
row = []
col = []
data = []
for indexes in index_list: #progressbar.progressbar(index_list):
    if len(indexes)>1:
        for i,ind1 in enumerate(indexes):
            for ind2 in indexes[i:]:
                row.append(ind1)
                col.append(ind2)
                data.append(1)
                row.append(ind2)
                col.append(ind1)
                data.append(1)              
                num += 1
co_occurance_matrix = coo_matrix((data,(row,col)),shape = (len(all_hashtags),len(all_hashtags)),dtype=float)
sparse.save_npz('co_occurance_matrix_short',co_occurance_matrix)
                
occurence = np.zeros(len(all_hashtags_list))
scaled_favs = np.zeros(len(all_hashtags_list))
scaled_rts = np.zeros(len(all_hashtags_list))
sf = df_eng['scaled_favs'].tolist()
sr = df_eng['scaled_rts'].tolist()

i = 0
for indexes in index_list: #progressbar.progressbar(index_list):
    for index in indexes:
        occurence[index] += 1
        scaled_favs[index] += sf[i]
        scaled_rts[index] += sr[i]
    i += 1
    
hashtag_df = pd.DataFrame({'hashtags':all_hashtags_list,'occurence':occurence,
                           'scaled_favs':scaled_favs,'scaled_rts':scaled_rts})
    
hashtag_df.to_csv('hashtags_short.csv')
occurence = hashtag_df['occurence'].tolist()
co_occurance_matrix = co_occurance_matrix.tocsr()


for i in range(co_occurance_matrix.shape[0]): #progressbar.progressbar(range(co_occurance_matrix.shape[0])): 
    co_occurance_matrix[i] = co_occurance_matrix[i]/float(occurence[i])
    
sparse.save_npz('co_occurance_norm_short',co_occurance_matrix)
