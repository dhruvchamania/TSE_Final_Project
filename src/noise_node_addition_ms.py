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

def noise_node_addition(k,l,n,I,cond,path):
    mem_before = helpers.get_process_memory()
    G = nx.read_gml(path)
    G_old = nx.read_gml(path)
    i = 0
    for node in G.nodes:
        G.add_node(node, label = (node[0],node[1]), degree = G.degree[node], id = i)
        i += 1
    start_time = time.time()
    initial_apl = 1
    if cond == 1:
        initial_apl = helpers.calculate_apl(G)
    if n == 1:
        G = helpers.generate_tds_onlyk(G,k,I)
    elif n == 2:
        G = helpers.generate_tds_kl(G,k,l,I)
    elif n == 3:
        G = helpers.generate_tds(G,k,l,I,3,0.25)
    dec_degree = []
    inc_degree = []
    for node in G.nodes:
        if G.node[node]['target_degree'] != G.node[node]['degree']:
            ## NEIGHBOR EDGE EDITING TECHNIQUE
            #print node
            nei = list(G.neighbors(node))
            for n in nei:
                if G.node[node]['target_degree'] == G.node[node]['degree'] - 1 and G.node[n]['target_degree'] == G.node[n]['degree'] - 1:  ## UNTESTED
                    G.remove_edge(node,n)
                    G.node[node]['degree'] = G.node[node]['degree'] - 1
                    G.node[n]['degree'] = G.node[n]['degree'] - 1
                    # print (G.node[node]['target_degree'], G.node[node]['degree'], G.degree(node))
                if G.node[node]['target_degree'] == G.node[node]['degree'] - 1 and G.node[n]['target_degree'] == G.node[n]['degree'] + 1:   ## UNTESTED
                    temp = list(set(G[node]) - set(G[n]))
                    #print temp
                    var = temp[0]                                              ## Can use var = random.choice(temp), but it causes randomness in result
                    #print var
                    G.remove_edge(node,var)
                    G.add_edge(n,var)
                    G.node[node]['degree'] = G.node[node]['degree'] - 1
                    G.node[n]['degree'] = G.node[n]['degree'] + 1               # allow to leave condition if temp empty
                    #print temp
#print G.nodes(data = True)
            neigh = nx.single_source_shortest_path_length(G,node,cutoff = 2)
            for key,value in neigh.items():                                            ## STEP 1, CASE 2
                if value == 2:
                    if G.node[node]['target_degree'] == G.node[node]['degree'] + 1 and G.node[key]['target_degree'] == G.node[key]['degree'] + 1:
                        #print G.node[node]['target_degree'], G.node[node]['degree'], G.node[key]['target_degree'], G.node[key]['degree']
                        G.add_edge(node, key)
                        G.node[node]['degree'] = G.node[node]['degree'] + 1
                        G.node[key]['degree'] = G.node[key]['degree'] + 1
                        #print G.node[node]['target_degree'], G.node[node]['degree'], G.node[key]['target_degree'], G.node[key]['degree']

            ## ADDING NOISE NODE TO DECREASE DEGREE

            if G.node[node]['target_degree'] < G.node[node]['degree']:
                dec_degree.append(node)
                #print dec_degree

            ## ADDING NOISE NODE TO INCREASE DEGREE

            if G.node[node]['target_degree'] > G.node[node]['degree']:
                inc_degree.append(node)
                #print inc_degree
    noise_node = 1
    for val in inc_degree:                                                        ## Adding noise nodes to Increase degree
        #print G.node[val]['target_degree'], G.node[val]['degree'], G.degree(val)
        neigh = nx.single_source_shortest_path_length(G,val,cutoff = 2)
        while G.node[val]['target_degree'] != G.node[val]['degree']:
            G.add_node(noise_node, type = "noise", degree = 1, target_degree = 0, label = random.choice(string.ascii_uppercase))        #check for alpha
            G.add_edge(val, noise_node)
            G.node[val]['degree'] = G.node[val]['degree'] + 1
            for key,value in neigh.items():
                if G.node[key]['target_degree'] > G.node[key]['degree'] and value>0:
                    G.add_edge(key, noise_node)
                    G.node[key]['degree'] = G.node[key]['degree'] + 1
                    G.node[noise_node]['degree'] = G.node[noise_node]['degree'] + 1
                    #print G.node[key]['target_degree'], G.node[key]['degree'], G.degree(key), value
            noise_node = noise_node + 1
            #print G.node[val]['target_degree'], G.node[val]['degree'], G.degree(val)
    for val in dec_degree:                                                        ## Adding noise nodes to Decrease degree (UNTESTED)
        G.add_node(noise_node, type = "noise", degree = 1, target_degree = 0, label = random.choice(string.ascii_uppercase))
        #G.add_edge(val, noise_node)
        count = 1
        m = G.node[val]['degree'] - G.node[val]['target_degree'] + 2
        #while G.node[val]['target_degree'] != G.node[val]['degree']:
        neighb = list(G.neighbors(val))
        for n in neighb:
            if count < m:
                G.remove_edge(val,n)
                G.add_edge(n, noise_node)
                G.node[val]['degree'] = G.node[val]['degree'] - 1
                G.node[noise_node]['degree'] = G.node[noise_node]['degree'] + 1
                count = count + 1
        G.add_edge(val, noise_node)
        G.node[val]['degree'] = G.node[val]['degree'] + 1
        noise_node = noise_node + 1

    new_apl = 0
    if cond==1:
        new_apl = helpers.calculate_apl(G)

    #Debugging
    # for node in G_new.nodes():
        # print (G_new.degree[node])
    #print(initial_apl,new_apl)
    error = (abs(new_apl-initial_apl)/initial_apl)*100
    end_time = time.time()
    mem_after = helpers.get_process_memory()
    x = end_time - start_time
    y = mem_after - mem_before

    return G_old, G , x, y, error
