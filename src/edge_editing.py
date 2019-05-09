## Aim of this script is to return an anonymised graph after performing Edge Editing. Essentially, this script uses the helpers
## function to obtain the target degree sequence. After this, we add random edges to fulfill this target degree sequence.


from __future__ import division
import networkx as nx
import collections
import random
import string
import matplotlib.pyplot as plt
from operator import itemgetter
from operator import attrgetter
from matplotlib import pyplot as plt
import time
from src import helpers
import time
import os
import psutil


def edge_editing(k,l,n,I,cond,path):
    '''

    '''

    mem_before = helpers.get_process_memory()
    G = nx.read_gml(path)
    G_old = nx.read_gml(path)
    #Debgging
    # print(1)
    labels = []
    i = 0
    for node in G.nodes:
        G.add_node(node, label = node[0], degree = G.degree[node], id = i)
        i += 1
        labels.append(G.node[node]['label'])
    #Debugging
    # print(2)
    start_time = time.time()
    initial_apl = 1
    if cond == 1:                                  ## Calculating Average Path Length of the original graph.
        #Debugging
        #print(1)
        initial_apl = helpers.calculate_apl(G)
        #Debugging
        #print(initial_apl)
    '''
    # original_cc = nx.average_clustering(G)
    # while p < number_runs:
    #G = nx.convert_node_labels_to_integers(H, label_attribute = 'author_name')
    #cloc = {}
    #cloc = nx.closeness_centrality(G)
    #cloc = sorted(cloc.items(), key = itemgetter(1), reverse = True)
    #btwc = {}
    #btwc = nx.betweenness_centrality(G)
    #btwc = sorted(btwc.items(), key = itemgetter(1), reverse = True)
    #eigc = {}
    #eigc = nx.eigenvector_centrality(G)
    #eigc = sorted(eigc.items(), key = itemgetter(1), reverse = True)
    #for node in G.nodes:
    #    G.add_node(node, clo_centrality = cloc[node], btw_centrality = btwc[node], eig_centrality = eigc[node])
    #print G.nodes(data = True)
                                            ## Taking input for K-Anonymity
    #alpha = input("Enter the value of alpha \n")                                   ## Taking input for Alpha
    #cent_measure = raw_input("Enter the centrality measure : \n")
    '''
    ## Generating the target degree sequence
    if n == 1:
        G = helpers.generate_tds_onlyk(G,k,I)
    elif n == 2:
        G = helpers.generate_tds_kl(G,k,l,I) 
    elif n == 3:
        G = helpers.generate_tds(G,k,l,I,3,0.25)
    edge_target = []
    
    for node in G.nodes():
        edge_target.append(G.node[node]['target_degree'])
        #Debugging
        # print(G.node[node])
    if sum(edge_target) % 2 != 0:
        edge_target[0] += 1
    G_new = nx.configuration_model(edge_target)
    i = 0
    for node in G_new.nodes:
        G_new.add_node(node, label = labels[i])
        i += 1
    new_apl = 0
    if cond == 1:
        #Debuggging
        # print(1)
        new_apl = helpers.calculate_apl(G_new)
        #print(new_apl)
    #Debugging
    # for node in G_new.nodes():
        # print (G_new.degree[node])
    #actual_centrality = []
    '''
    for i in helpers.centrality_top_20(G_old):
        actual_centrality.append(G.node[i[0]]['id'])
    print("New apl",new_apl)
    print("Original apl",initial_apl)
    print("Top 20 centrality in original graph", actual_centrality)
    print("Top 20 centrality in new graph", helpers.centrality_top_20(G_new))
    '''
    end_time = time.time()
    mem_after = helpers.get_process_memory()
    x = end_time - start_time
    y = mem_after - mem_before
    error = (abs(new_apl-initial_apl)/initial_apl)*100
    return G_old, G_new , x, y,error
