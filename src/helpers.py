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

#Calculate the Average Path Length of both connected and disconnected graphs

def calculate_apl(G):
    """

    :param G: The networkx graph
    :return: Calculated apl
    """
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

# Returns the centrality values of the nodes in the graph depending on the type of centrality chosen.
def centralitity(G,i):
    """

    :param G: The networkx graph
    :param i: Which centrality
    :return: the dictory with vertices
    """
    degc = {}
    
    if i == 1:
        #print("Making use of eigenvector centrality")
        degc = nx.eigenvector_centrality(G)
    elif i == 2:
        #print("Making use of closeness centrality")
        degc = nx.closeness_centrality(G)
    elif i == 3:
        #print("Making use of betweenness centrality")
        degc = nx.betweenness_centrality(G)
    elif i == 4:
        #print("Making use of degree centrality")
        degc = nx.degree_centrality(G)
    else:
        #print("Making use of katz centrality")
        degc = nx.katz_centrality_numpy(G)

    return degc

## Plotting the graph with the labels

def plot_graph(G):
    """
    :param G: The networkx graph to plot
    :return: The plotted graph
    """
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

def get_title(i,j):

    I = ['Only k','K & l', 'All ']
    J = ['Eigen','closeness','betweeness','degree','katz']
    s = 'Using ' + I[i] + ' and ' + J[j] + ' centrality'
    return s

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

# Generates the target degree sequence for given values of hyperparameters using all available privacy measures
def generate_tds(G,k,l,i,c_var = 3, alpha = 0.25):
    """

    :param G: Networkx Graph
    :param k: The value of k degree anonimity
    :param l: The value of l diversity
    :param i: The value of centrality
    :param c_var: value of c in recursive cl diversity
    :param alpha: value of alpha anonimity
    :return: Networkx Graph
    """

    #print("Using all for privacy measures")
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
    #Debugging
    # print("Hello")
    for val in degc:
        if count > k:                                                          ## Adding K-Anonymity
            c = collections.Counter(labels_present)
            target_label_count = c.most_common(1)[0][1]                        ## count of the most frequent label
            #Debugging
            # print target_label_count / (count - 1), count                      ## debugging
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

# Generates the target degree sequence for given values of hyperparameters using only K-degree anonymity privacy measure

def generate_tds_onlyk(G,k,i):
    """

    :param G: Networkx Graph
    :param k: The value of k degree anonimity
    :param i: The centrality
    :return: Networkx Graph
    """
    #print("Using only k privacy measures")
    degc = {}
    #Debugging
    # print(i)
    degc = centralitity(G,i)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    target = G.node[degc[0][0]]['degree']                                      ## For the first time, setting target degree
    count = 1                                                                  ## Count denotes number of nodes in each equivalence group
    #Debugging
    # print("Hello")
    for val in degc:
        if count > k:                                                          ## Adding K-Anonymity
            target = G.node[val[0]]['degree']
            count = 1
        G.add_node(val[0], target_degree = target)
        count = count + 1
    return G

## Generates the target degree sequence for given values of hyperparameters using K-degree anonymity and L-diversity privacy measures

def generate_tds_kl(G,k,l,i):
    """

    :param G: Networkx Graph
    :param k: The value of k degree anonimity
    :param l: The value of l diversity
    :param i: The value of centrality
    :return: Networkx Graph
    """
    #print("Using k,l privacy measures")
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
    #Debugging
    # print("Hello")
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

# Returns the top 20 nodes in the graph with the best centrality values 

def centrality_top_20(G):
    degc = nx.degree_centrality(G)
    degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
    return degc[:20]

#Returns the number of nodes which remain in the best 20 centrality valued nodes after anonymisation

def centrality_top_20_compare(G_old,G_new):
    """

    :param G_old: The old graph
    :param G_new: The new graph
    :return: The count of the top 20 same values
    """
    old,new = [],[]
    I = 0
    for node in G_old.nodes:
        G_old.add_node(node, id = I,label = node[0])
        I += 1

    I = 0
    for node in G_new.nodes:
        G_new.add_node(node, id = I)
        I += 1
    #Debugging
    # print("Hello")
    for i in centrality_top_20(G_old):
        old.append(G_old.node[i[0]]['id'])
    for i in centrality_top_20(G_new):
        #print(i)
        new.append(G_new.node[i[0]]['id'])
        # new.append(i[0])
    #Debugging
    #print(old,new)
    old,new = set(old),set(new)
    res = old.intersection(new)
    return len(res)

def centrality_values(G):
    """

    :param G: Networkx Graph
    :return: Plotted Graph
    """
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
            #Debugging
            # print G.degree(n), G.node[n]['degree'], G.node[n]
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

def plot_graph2(G1,G2, Title="Default Title"):
    """

    :param G1: The old networkx graph
    :param G2: The new networkx graph
    :param Title: THe title contating which centrality
    :return: Plotted Graph
    """

    fig = plt.figure(figsize=(40,40))
    fig.suptitle(Title, fontsize=20, fontweight='bold')

    ax1 = fig.add_subplot(121)
    ax1.set_title("Original Graph")

    pos_nodes = nx.spring_layout(G1)
    nx.draw(G1, pos_nodes, with_labels=True)

    pos_attrs = {}
    for node, coords in pos_nodes.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.08)

    node_attrs = nx.get_node_attributes(G1, 'label')
    custom_node_attrs = {}
    #print(len(node_attrs))
    for node, attr in node_attrs.items():
        custom_node_attrs[node] = "{'label': '" + attr + "'}"

    nx.draw_networkx_labels(G1, pos_attrs, labels=custom_node_attrs, ax=ax1, with_labels = True)


    ###########

    ax2 = fig.add_subplot(122)
    ax2.set_title("Modified Graph")

    pos_nodes = nx.spring_layout(G2)
    nx.draw(G2, pos_nodes, with_labels=True)

    pos_attrs = {}
    for node, coords in pos_nodes.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.08)

    node_attrs = nx.get_node_attributes(G2, 'label')
    custom_node_attrs = {}
    for node, attr in node_attrs.items():
        custom_node_attrs[node] = "{'label': '" + attr + "'}"

    nx.draw_networkx_labels(G2, pos_attrs, labels=custom_node_attrs, ax=ax2)

    plt.show()

def plot_graph_summary(G1,Gs, Titles=[]):
    """

    :param G1: The Old Graph
    :param Gs: The list of all graphs
    :param Titles: The title of graphs
    :return: The plotted graphs
    """

    fig = plt.figure(figsize=(50,50))
    fig.suptitle("SUMMARY", fontsize=15, fontweight='bold')

    for i in range(15):
        row = i//5
        col = i%5

        if Titles:
            title=Titles.pop(0)
        else:
            title="Default Title"

        ax = plt.subplot2grid((3,5),(row,col))

        ax.set_title(title, fontsize=10)

        g = Gs[i]

        pos_nodes = nx.spring_layout(g)
        nx.draw(g, pos_nodes, with_labels=True)

        pos_attrs = {}
        for node, coords in pos_nodes.items():
            pos_attrs[node] = (coords[0], coords[1] + 0.08)

        node_attrs = nx.get_node_attributes(g, 'label')
        custom_node_attrs = {}
        for node, attr in node_attrs.items():
            custom_node_attrs[node] = "{'label': '" + attr + "'}"

        nx.draw_networkx_labels(g, pos_attrs, labels=custom_node_attrs, ax=ax)

    plt.show()
