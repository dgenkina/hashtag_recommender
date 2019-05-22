# -*- coding: utf-8 -*-
"""
Created on Wed May 22 00:25:18 2019

@author: swooty
"""
import numpy as np
from scipy import sparse
from scipy.sparse import coo_matrix
import pandas as pd
import matplotlib.pyplot as plt
import progressbar


co_occurance_matrix = sparse.load_npz('co_occurance_norm.npz')
hashtag_df = pd.read_csv('hashtags.csv')
hashtags = hashtag_df['hashtags'].tolist()
scaled_favs = hashtag_df['scaled_favs'].tolist()
scaled_rts = hashtag_df['scaled_rts'].tolist()
occurence = hashtag_df['occurence'].tolist()

#KeepItLIT,myhittamyhitta,craftbeer
tag = np.random.choice(hashtag_df.loc[pd.notnull(hashtag_df['scaled_rts']),'hashtags'].tolist())
tag_ind = hashtags.index(tag)
print(hashtags[tag_ind])
print(scaled_favs[tag_ind])
print(scaled_rts[tag_ind])
for ind,co in enumerate(co_occurance_matrix[tag_ind].toarray()[0]):
    if co>0:
        if ind != tag_ind:
            print(hashtags[ind])
            print(scaled_favs[ind])
            print(scaled_rts[ind])
            if scaled_favs[ind]>scaled_favs[tag_ind]:
                print(hashtags[ind])
            elif scaled_rts[ind]>scaled_rts[tag_ind]:
                print(hashtags[ind])
            
    


