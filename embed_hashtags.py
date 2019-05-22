# -*- coding: utf-8 -*-
"""
Created on Tue May 21 18:21:01 2019

@author: swooty
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from matplotlib import gridspec 
import scipy

featureFile = np.load('hashtag_features.npz')
X = scipy.sparse.load_npz('hashtag_tfidf.npz')
hashtags = featureFile['hashtag_list']

X_embed = TSNE(n_components=2,method='exact').fit_transform(X)


figure = plt.figure()
pan = figure.add_subplot(111)
pan.scatter(X_embed[:,0], X_embed[:,1], s=2)
pan.set_xticks([])
pan.set_yticks([])