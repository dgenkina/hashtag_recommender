# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 11:01:13 2019

@author: Swooty
"""
from scipy import sparse
from scipy.sparse import dok_matrix, coo_matrix
import numpy as np
from itertools import combinations
import progressbar
import itertools 
import networkx as nx
import pickle

def nodes_connected(graph, u, v):
     return u in graph.neighbors(v)
 

def make_graph(hashtag_list_of_lists,success_list,timestamp_list,savename='instagraph'):
    tag_graph = nx.Graph()
    for ind,hashtag_list in progressbar.progressbar(enumerate(hashtag_list_of_lists)):
        for hashtag in hashtag_list:
            if hashtag in tag_graph.nodes:
                success = tag_graph.nodes[hashtag]['success'] + success_list[ind]
                occurence = tag_graph.nodes[hashtag]['occurence'] + 1.0
                
                successes = list(tag_graph.nodes[hashtag]['successes'])
                successes.append(success_list[ind])
                successes = tuple(successes)
                
                timestamps = list(tag_graph.nodes[hashtag]['timestamps'])
                timestamps.append(timestamp_list[ind])
                timestamps = tuple(timestamps)
                
            else:
                success = success_list[ind]
                occurence = 1.0  
                successes = tuple([success_list[ind]])
                timestamps = tuple([timestamp_list[ind]])
            tag_graph.add_node(hashtag, success=success,occurence=occurence,
                              successes = successes, timestamps=timestamps)
        
        for a,b in itertools.combinations(hashtag_list,2):
            if nodes_connected(tag_graph,a,b):
                tag_graph[a][b]['weight']+=1
            else:
                tag_graph.add_edge(a,b,weight=1)
    with open(savename, 'wb') as f:
        pickle.dump(tag_graph,f)
    return tag_graph
    
    
def make_index_list_of_lists(hashtag_list_of_lists, savename = 'hashtags_and_indeces'):
    all_hashtags = set().union(*hashtag_list_of_lists)
    all_hashtags_list = list(all_hashtags)
        
    index_list_of_lists = []
    for hashtag_list in progressbar.progressbar(hashtag_list_of_lists):
        local_list = []
        for ind, hashtag in enumerate(hashtag_list):
            ind = all_hashtags_list.index(hashtag)
            local_list.append(ind)
        index_list_of_lists.append(local_list)
    np.savez(savename,all_hashtags_list=all_hashtags_list,index_list_of_lists=index_list_of_lists)
    return all_hashtags_list, index_list_of_lists


def get_hashtag_stats(success_list, hashtags_and_indeces_filename = 'hashtags_and_indeces',savename = 'occurence_and_success'):
    filedict = np.load(hashtags_and_indeces_filename+'.npz')
    all_hashtags_list = filedict['all_hashtags_list']
    index_list_of_lists = filedict['index_list_of_lists']
    occurence_of_tags = np.zeros(len(all_hashtags_list))
    success_scores_of_tags = np.zeros(len(all_hashtags_list))
    i = 0
    for index_list in progressbar.progressbar(index_list_of_lists):
        for index in index_list:
            occurence_of_tags[index] += 1
            success_scores_of_tags[index] += success_list[i]
        i += 1
    np.savez(savename,occurence_of_tags=occurence_of_tags,success_scores_of_tags=success_scores_of_tags)
    return occurence_of_tags, success_scores_of_tags    
    

def make_cooccurence_matrix(occurence_and_success_filename = 'occurence_and_success',
                            hashtags_and_indeces_filename = 'hashtags_and_indeces',
                            savename='cooccurence_matrix'):

    index_list_of_lists = np.load(hashtags_and_indeces_filename+'.npz')['index_list_of_lists']
    occurence_of_tags = np.load(occurence_and_success_filename+'.npz')['occurence_of_tags']
    num = 0
    row = []
    col = []
    data = []
    max_ind = 0
    
    for index_list in progressbar.progressbar(index_list_of_lists):
        if max(index_list) > max_ind:
            max_ind = max(index_list)
        if len(index_list)>1:
            for ind1,ind2 in combinations(index_list,2):
                norm = occurence_of_tags[ind1]*occurence_of_tags[ind2]
                row.append(ind1)
                col.append(ind2)
                data.append(1.0/norm)
                row.append(ind2)
                col.append(ind1)
                data.append(1.0/norm)              
                num += 1
    shape = (len(occurence_of_tags),len(occurence_of_tags))
    co_occurence_matrix = coo_matrix((data,(row,col)),shape = shape,dtype=float)
    co_occurence_matrix = co_occurence_matrix.tocsr()
    sparse.save_npz(savename,co_occurence_matrix)
    return co_occurence_matrix

def recommend(hashtag = None, 
              matrix_filename='cooccurence_matrix', 
              hashtag_filename='hashtags_and_indeces',
              occurence_and_success_filename='occurence_and_success'):
    
    co_occurance_matrix = sparse.load_npz(matrix_filename+'.npz')
    hashtags =np.load(hashtag_filename+'.npz')['all_hashtags_list']
    success = np.load(occurence_and_success_filename+'.npz')['success_scores_of_tags']
    occurence = np.load(occurence_and_success_filename+'.npz')['occurence_of_tags']
    
    if hashtag is None:
        tag = np.random.choice(hashtags)
    else:
        tag = hashtag
        
    tag_ind = list(hashtags).index(tag)
    score_tag = success[tag_ind]/occurence[tag_ind]
    print('For hashtag #{tag} with success score of {score} and occurence of {occur}:'.format(tag=hashtags[tag_ind],
          score = score_tag,
          occur = occurence[tag_ind]))
    
    for ind,co in enumerate(co_occurance_matrix[tag_ind].toarray()[0]):
        if co>0:
            score_other = success[ind]/occurence[ind]
            if ind != tag_ind and score_other>score_tag:
                print()
                print('Similar hashtag #{tag} has success score of {score}'.format(tag=hashtags[ind],score=score_other))
                print('Co-occurence matrix element of {co}'.format(co=co))
