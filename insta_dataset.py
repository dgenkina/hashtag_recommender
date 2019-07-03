# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:47:35 2019

@author: Swooty
"""

import pandas as pd
import sys
from recommender_functions import *
filepath = 'C:\\Users\\Swooty\\Documents\\Data science\\DataIncubator\\twitter\\insta_data\\media.csv'
#
#with open(filepath, 'a') as file:
#    string = file.read()
df = pd.read_csv(filepath, sep=';', encoding='iso-8859-1')

df_has_tags = df.loc[pd.notnull(df['comments'])]
df_has_tags['tagset'] = df_has_tags['tagset'].apply(lambda x: x.split(','))

first_1000_posts = df_has_tags['tagset'].tolist()[0:10]

all_hashtags_list, index_list_of_lists = make_index_list_of_lists(first_1000_posts)

likes_list = df_has_tags['likes'].tolist()[0:10]
occurence_of_tags, likes_of_tags = get_hashtag_stats(likes_list)

co_occurence_matrix = make_cooccurence_matrix(savename='co_occurence_matrix_insta_small')

recommend(hashtag = None, 
              matrix_filename='co_occurence_matrix_insta_small', 
              hashtag_filename='hashtags_and_indeces',
              occurence_and_success_filename='occurence_and_success')