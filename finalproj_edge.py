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

def edge_editing(k,l,path):
    
    G = nx.read_gml(path)
    G_old = nx.read_gml(path)
    for node in G.nodes:
        G.add_node(node, label = node[0], degree = G.degree[node])

    start_time = time.time()
    k_val = []
    apl_val = []
    raw_apl = []
    # original_centrality_val = []
    # noise_centrality_val = []
    # p = 0
    #
    add = 0
    lol = 0
    max_order = 2

    #Checking to see if the graph is connected or not
    if nx.is_connected(G):
        add = 1
        lol = 1

    else:
        for g in nx.connected_component_subgraphs(G):
            if g.order() > 2:
                add = add + nx.average_shortest_path_length(g)
                lol = lol + 1
                if g.order() > max_order:
                    max_order = g.order()
                    original_center = nx.center(g)

    initial_apl = add/lol

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
    alpha = 0.25
    
    k_val.append(k)
    degc = {}
    degc = nx.eigenvector_centrality(G)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    target = G.node[degc[0][0]]['degree']                                      ## For the first time, setting target degree
    labels_present = []
    targets_present = []
    temp_labels_present = []
    count = 1                                                                  ## Count denotes number of nodes in each equivalence group
    c_var = 3
    print("Hello")
    for val in degc:
        if count > k:                                                          ## Adding K-Anonymity
            c = collections.Counter(labels_present)
            target_label_count = c.most_common(1)[0][1]                        ## count of the most frequent label
            #print target_label_count / (count - 1), count                      ## debugging
            temp_count = 0
            recursive_sum = 0
            dict(c)
            for key,valuee in c.items():                                            ## For recursive c-l diversity
                if temp_count >= l:
                    recursive_sum = recursive_sum + valuee
                    temp_count = temp_count + 1
                else:
                    temp_count = temp_count + 1
            if  target_label_count/(count-1) < alpha and len(temp_labels_present) >= l : #and target_label_count < (c_var*recursive_sum):                           ## Alpha Anonymity condition, count - 1 is used because the count is always 1 ahead of the actual number of nodes
                target = G.node[val[0]]['degree']
                count = 1
                del labels_present[:]
                del temp_labels_present[:]
        G.add_node(val[0], target_degree = target)
        labels_present.append(G.node[val[0]]['label'])                        ## All the labels present in the equivalence group
        if G.node[val[0]]['target_degree'] not in targets_present:
            targets_present.append(G.node[val[0]]['target_degree'])
        if G.node[val[0]]['label'] not in temp_labels_present:
            temp_labels_present.append(G.node[val[0]]['label'])               ## No of distinct labels present in the equivalence group
        count = count + 1
    edge_target = []
    for node in G.nodes():
        edge_target.append(G.node[node]['target_degree'])
        # print(G.node[node])
    # G_new = nx.havel_hakimi_graph(edge_target)
    # if not nx.is_valid_degree_sequence(edge_target):
    edge_target[0] += 1
    G_new = nx.configuration_model(edge_target)

    add = 0
    lol = 0
    max_order = 2
    for g in nx.connected_component_subgraphs(G_new):
        if g.order() > 2:
            add = add + nx.average_shortest_path_length(g)
            lol = lol + 1
            if g.order() > max_order:
                max_order = g.order()
                original_center = nx.center(g)
    #print add / lol, lol
    new_apl = add/lol
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

G1,G2 = edge_editing(k,l,'netscience.gml')
print(len(G1.nodes), len(G2.nodes))
print(len(G1.edges), len(G2.edges))
nx.draw_networkx(G1, with_labels=False)
plt.show()

nx.draw_networkx(G2,with_labels=False)
plt.show()
