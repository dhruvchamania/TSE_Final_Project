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
import helpers



def edge_editing(k,l,path):
    
    G = nx.read_gml(path)
    G_old = nx.read_gml(path)
    for node in G.nodes:
        G.add_node(node, label = node[0], degree = G.degree[node])

    start_time = time.time()
    
    apl_val = []
    raw_apl = []
    # original_centrality_val = []
    # noise_centrality_val = []
    # p = 0
    #
    initial_apl = helpers.calculate_apl(G)
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
    
    G = helpers.generate_tds(G,k,l,)
    edge_target = []
    for node in G.nodes():
        edge_target.append(G.node[node]['target_degree'])
        # print(G.node[node])
    # G_new = nx.havel_hakimi_graph(edge_target)
    # if not nx.is_valid_degree_sequence(edge_target):
    edge_target[0] += 1
    G_new = nx.configuration_model(edge_target)

    #print add / lol, lol
    new_apl = helpers.calculate_apl(G_new)
    # for node in G_new.nodes():
        # print (G_new.degree[node])
    print("New apl",new_apl)
    print("Original apl",initial_apl)
    end_time = time.time()
    print(end_time - start_time)

    return G_old, G_new    


G1 = nx.Graph()
G2 = nx.Graph()

k = int(input("Enter the value of k \n"))   
l = int(input("Enter the value of l \n"))

G1,G2 = edge_editing(k,l,r'..\data\netscience.gml')
print(len(G1.nodes), len(G2.nodes))
print(len(G1.edges), len(G2.edges))
nx.draw_networkx(G1, with_labels=False)
plt.show()

nx.draw_networkx(G2,with_labels=False)
plt.show()
