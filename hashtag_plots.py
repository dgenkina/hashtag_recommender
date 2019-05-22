# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:14:38 2019

@author: swooty
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy.sparse import dok_matrix
import progressbar
import matplotlib.gridspec as gridspec


df = pd.read_csv('hashtags.csv')
tweet_num = 172206.0

occurence = df['occurence'].tolist()
hashtags = df['hashtags'].tolist()
sort = np.argsort(occurence)
occurs = np.array(occurence)[sort[-15:-1]]/tweet_num
tags = np.array(hashtags)[sort[-15:-1]]

fig = plt.figure()
fig.clear()
fig.set_size_inches(7.0,5.0)
gs = gridspec.GridSpec(1,1)
gs.update(left=0.15, right=0.95, top=0.9, bottom = 0.25)
gs.update(hspace=0.2,wspace=0.5)
pan = fig.add_subplot(gs[0])
pan.plot(np.arange(occurs.size), occurs, 'bo')
pan.set_xticks(np.arange(occurs.size))
pan.set_xticklabels(tags)
pan.set_ylabel('Fraction of tweets')
pan.set_title('Most common hashtags in dataset')
plt.xticks(rotation = 60)
plt.savefig('Most common hashtags.pdf',transparent=True)

scaled_favs_sort = df.sort_values(by='scaled_favs', ascending=False)
favs = scaled_favs_sort['scaled_favs'].tolist()[0:15]
tags = scaled_favs_sort['hashtags'].tolist()[0:15]

fig = plt.figure()
fig.clear()
fig.set_size_inches(7.0,5.0)
gs = gridspec.GridSpec(1,1)
gs.update(left=0.15, right=0.95, top=0.9, bottom = 0.35)
gs.update(hspace=0.2,wspace=0.5)
pan = fig.add_subplot(gs[0])
pan.plot(np.arange(len(favs)), favs, 'bo')
pan.set_xticks(np.arange(len(favs)))
pan.set_xticklabels(tags)
pan.set_ylabel('Totals favs/followers')
pan.set_title('Most liked hashtags in dataset')
plt.xticks(rotation = 80)
plt.savefig('Most liked hashtags.pdf',transparent=True)

scaled_rts_sort = df.sort_values(by='scaled_rts', ascending=False)
rts = scaled_rts_sort['scaled_rts'].tolist()[0:15]
tags = scaled_rts_sort['hashtags'].tolist()[0:15]

fig = plt.figure()
fig.clear()
fig.set_size_inches(7.0,5.0)
gs = gridspec.GridSpec(1,1)
gs.update(left=0.15, right=0.95, top=0.9, bottom = 0.35)
gs.update(hspace=0.2,wspace=0.5)
pan = fig.add_subplot(gs[0])
pan.plot(np.arange(len(rts)), rts, 'bo')
pan.set_xticks(np.arange(len(rts)))
pan.set_xticklabels(tags)
pan.set_ylabel('Totals rts/followers')
pan.set_title('Most re-tweeted hashtags in dataset')
plt.xticks(rotation = 80)
plt.savefig('Most liked hashtags.pdf',transparent=True)

