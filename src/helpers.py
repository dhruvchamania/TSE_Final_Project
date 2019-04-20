from __future__ import division
import networkx as nx
import collections
import random
import string
from operator import itemgetter
from matplotlib import pyplot as plt

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
                    original_center = nx.center(g)

    return add/lol

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

def generate_tds(G,k,l,c_var  =3,alpha = 0.25):
    k_val = []
    k_val.append(k)
    degc = {}
    degc = nx.eigenvector_centrality(G)
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
    return G

def generate_tds_onlyk(G,k):
    degc = {}
    degc = nx.eigenvector_centrality(G)
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
    # noise_cc = nx.average_clustering(G)
    l_5 = plt.plot(k_val[0:4], noise_centrality_val[0:4], label = 'l = 5', marker = '*')
    l_10 = plt.plot(k_val[4:], noise_centrality_val[4:], label = 'l = 10', marker = '+')
    raw_graph = plt.plot(k_val, original_centrality_val, label = 'Raw Graph')
    plt.xlabel('Values of K')
    plt.ylabel('Social Importance')
    plt.legend()
    plt.show()
