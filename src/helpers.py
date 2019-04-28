from __future__ import division
import networkx as nx
import collections
import random
import string
from operator import itemgetter
from matplotlib import pyplot as plt
import time
import os
import psutil

mem = []
def calculate_apl(G):
    add = 0
    lol = 0
    max_order = 2

    #Checking to see if the graph is connected or not
    if nx.is_connected(G):
        return nx.average_shortest_path_length(G)

    else:
        for g in nx.connected_component_subgraphs(G):
            if g.order() > 2:
                add = add + nx.average_shortest_path_length(g)
                lol = lol + 1
                if g.order() > max_order:
                    max_order = g.order()

    return add/lol

def centralitity(G,i):

    degc = {}
    
    if i == 1:
        print("Making use of eigenvector centrality")
        degc = nx.eigenvector_centrality(G)
    elif i == 2:
        print("Making use of closeness centrality")
        degc = nx.closeness_centrality(G)
    elif i == 3:
        print("Making use of betweenness centrality")
        degc = nx.betweenness_centrality(G)
    elif i == 4:
        print("Making use of degree centrality")
        degc = nx.degree_centrality(G)
    else:
        print("Making use of katz centrality")
        degc = nx.katz_centrality(G)

    return degc


def plot_graph(G):
    plt.figure()
    pos_nodes = nx.spring_layout(G)
    nx.draw(G, pos_nodes, with_labels=True)

    pos_attrs = {}
    for node, coords in pos_nodes.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.08)

    node_attrs = nx.get_node_attributes(G, 'label')
    custom_node_attrs = {}
    for node, attr in node_attrs.items():
        custom_node_attrs[node] = "{'label': '" + attr + "'}"

    nx.draw_networkx_labels(G, pos_attrs, labels=custom_node_attrs)
    plt.show()

def get_mem():
    return mem
    
def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        result = func(*args, **kwargs)
        mem_after = get_process_memory()
        mem.append(mem_after - mem_before)
        return result
    return wrapper
def generate_tds(G,k,l,i,c_var = 3, alpha = 0.25):

    print("Using all for privacy measures")
    k_val = []
    k_val.append(k)
    degc = {}
    degc = centralitity(G,i)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    target = G.node[degc[0][0]]['degree']                                      ## For the first time, setting target degree
    labels_present = []
    targets_present = []
    temp_labels_present = []
    count = 1                                                                  ## Count denotes number of nodes in each equivalence group
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
                key = 0
                if temp_count >= l:
                    recursive_sum = recursive_sum + valuee
                    temp_count = temp_count + key + 1
                else:
                    temp_count = temp_count + 1
            if  target_label_count/(count-1) < alpha and len(temp_labels_present) >= l and target_label_count < (c_var*recursive_sum):                           ## Alpha Anonymity condition, count - 1 is used because the count is always 1 ahead of the actual number of nodes
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
    return G

def generate_tds_onlyk(G,k,i):        #Not Tested
    print("Using only k privacy measures")
    degc = {}
    print(i)
    degc = centralitity(G,i)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    target = G.node[degc[0][0]]['degree']                                      ## For the first time, setting target degree
    count = 1                                                                  ## Count denotes number of nodes in each equivalence group
    print("Hello")
    for val in degc:
        if count > k:                                                          ## Adding K-Anonymity
            target = G.node[val[0]]['degree']
            count = 1
        G.add_node(val[0], target_degree = target)
        count = count + 1
    return G

def generate_tds_kl(G,k,l,i):         #Not Tested
    print("Using k,l privacy measures")
    k_val = []
    k_val.append(k)
    degc = {}
    degc = centralitity(G,i)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    target = G.node[degc[0][0]]['degree']                                      ## For the first time, setting target degree
    labels_present = []
    targets_present = []
    temp_labels_present = []
    count = 1                                                                  ## Count denotes number of nodes in each equivalence group
    print("Hello")
    for val in degc:
        if count > k:                                                          ## Adding K-Anonymity
            c = collections.Counter(labels_present)
            #Debugging
            #target_label_count = c.most_common(1)[0][1]                        ## count of the most frequent label
            #print target_label_count / (count - 1), count                 
            dict(c)
            if  len(temp_labels_present) >= l:
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
    return G

def centrality_top_20(G):
    degc = nx.degree_centrality(G)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    return degc[:20]

def centrality_values(G):
    original_centrality_val = []
    noise_centrality_val = []
    res = 0
    cnt = 0
    res_original_nodes = 0
    cnt_original_nodes = 0
    color_map = []
    degc = {}
    degc = nx.katz_centrality_numpy(G)
    for n in G.nodes():
        if G.node[n]['target_degree'] == 0 and G.node[n]['degree'] >=1:
            color_map.append('blue')
            res = res + degc[n]
            cnt = cnt + 1
            #print G.degree(n), G.node[n]['degree'], G.node[n]
        else:
            color_map.append('red')
            res_original_nodes = res_original_nodes + degc[n]
            cnt_original_nodes = cnt_original_nodes + 1

    original_centrality_val.append(res_original_nodes / cnt_original_nodes)
    noise_centrality_val.append(res / cnt)
    plt.xlabel('Values of K')
    plt.ylabel('Social Importance')
    plt.legend()
    plt.show()

