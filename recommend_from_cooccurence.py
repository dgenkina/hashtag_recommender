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


co_occurance_matrix = sparse.load_npz('co_occurance_matrix.npz')
hashtag_df = pd.read_csv('hashtags.csv')

for i in progressbar.progressbar(range(co_occurance_matrix.tocsr().shape[0])): 
    co_occurance_matrix.tocsr()[i]/float(i+1.0)