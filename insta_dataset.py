# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:47:35 2019

@author: Swooty
"""
import numpy as np
import pandas as pd
import sys
from recommender_functions import *
import progressbar
import pickle
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
from matplotlib import rcParams

filepath = 'C:\\Users\\Swooty\\Documents\\Data science\\DataIncubator\\twitter\\insta_data\\media.csv'
df = pd.read_csv(filepath, sep=';', encoding='iso-8859-1')

filepath = 'C:\\Users\\Swooty\\Documents\\Data science\\DataIncubator\\twitter\\insta_data\\users.csv'
df2 = pd.read_csv(filepath, sep=';', encoding='iso-8859-1')

df_followers = df2.groupby(['sID']).count()

df_has_tags = df[pd.notnull(df['comments'])]
df_has_tags['tagset'] = df_has_tags['tagset'].apply(lambda x: x.split(','))

def get_followers(author_id):
    try:
        followers = df_followers['tID'][author_id]
    except(KeyError):
        followers = 1.0
    return followers
df_has_tags['followers'] = df_has_tags['id_author'].apply(get_followers)
df_has_tags['scaled_likes'] = df_has_tags['likes']/df_has_tags['followers']

df_has_tags = df_has_tags.sample(frac=1).reset_index(drop=True)

graph_lo = 0
graph_hi = 300000
hashtag_lil = df_has_tags['tagset'].tolist()[graph_lo:graph_hi]
likes_list = df_has_tags['scaled_likes'].tolist()[graph_lo:graph_hi]
timestamp_list = df_has_tags['TS_upload'].tolist()[graph_lo:graph_hi]
followers_list = df_has_tags['followers'].tolist()[graph_lo:graph_hi]

savename = 'instagraph_300K'

try:
    with open(savename, 'rb') as f:
        graph = pickle.load(f)
except(FileNotFoundError):
    graph = make_graph(hashtag_lil,likes_list,timestamp_list,savename=savename)    



def get_hashtag_success(hashtag_list):
    summ = 0.0
    num = 0.0
    for ind, node in enumerate(hashtag_list):
        try:
            summ += float(graph.nodes[node]['success'])/float(graph.nodes[node]['occurence'])
            num += 1.0
        except(KeyError):
            pass
    if num == 0.0:
        return float('NaN')
    return summ

fit_lo = graph_hi
fit_hi = graph_hi + 100000
df_has_tags['hashtag_success'] = df_has_tags['tagset'].apply(get_hashtag_success)

y = df_has_tags[pd.notnull(df_has_tags['hashtag_success'])]['scaled_likes'][fit_lo:fit_hi]
X =df_has_tags[pd.notnull(df_has_tags['hashtag_success'])][['hashtag_success']][fit_lo:fit_hi]

lr = LinearRegression()
lr.fit(X,y)
print('Score = {score}'.format(score = lr.score(X,y)))
print('Coef = {coef}, intersept = {ic}'.format(coef = lr.coef_, ic = lr.intercept_))

test_lo = fit_hi
test_hi = fit_hi +100000
y_test = df_has_tags[pd.notnull(df_has_tags['hashtag_success'])]['scaled_likes'][test_lo:test_hi]
X_test = df_has_tags[pd.notnull(df_has_tags['hashtag_success'])][['hashtag_success']][test_lo:test_hi]
test_sc = lr.score(X_test,y_test)
print('Score on test set = {score}'.format(score = test_sc))

filepath = 'C:\\Users\\Swooty\\Documents\\Data science\\DataIncubator\\twitter\\insta_data\\users.csv'
df = pd.read_csv(filepath, sep=';', encoding='iso-8859-1')


rcParams['axes.labelsize'] = 20
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['legend.fontsize'] = 15

rcParams['pdf.fonttype'] = 42 # True type fonts
rcParams['font.family'] = 'sans-serif'

fig = plt.figure()
pan = fig.add_subplot(111)
pan.plot(X_test/10000,y_test/1000, 'r.',label = 'test data')
pan.plot(X/10000,y/1000, 'b.', label = 'fit data')
start,stop = pan.get_xlim()
xlist = np.linspace(start*1000,stop*10000, 1000)
ylist = lr.intercept_ + lr.coef_[0]*xlist
pan.plot(xlist/10000,ylist/1000,'b-')
pan.set_xlabel('Hashtag popularity score')
pan.set_ylabel('Post popularity score')
pan.set_title(r'$R^2$ score = {:.2f}'.format(test_sc), size = 20)
plt.legend()
fig.show()
plt.savefig('validation.png',dpi=500)






