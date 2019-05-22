# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:10:07 2019

@author: swooty
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy.sparse import dok_matrix
import progressbar
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer




df = pd.read_csv('dashboard_x_usa_x_filter_nativeretweets.csv')
df_eng = df.loc[df['Tweet language (ISO 639-1)']=='en']

tweets = df_eng['Tweet content']
hashtags_str = []
for tweet in tweets:
    tweet = tweet.decode('iso-8859-1')
    #print(tweet)
    local_str = ''
    ind = 0
    for tweet_word in tweet.split():
        if tweet_word.startswith("#"):
            ind += 1
            local_str = local_str + tweet_word.strip("#") + ' '
    if ind>1:
        hashtags_str.append(local_str)
#df_eng['hashtags_str'] = hashtags_str


tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(hashtags_str)
X_tfidf = X_tfidf.transpose()
hashtag_list = tfidf_vectorizer.get_feature_names()
np.savez('hashtag_features',hashtag_list=hashtag_list)

scipy.sparse.save_npz('hashtag_tfidf',X_tfidf)
                  