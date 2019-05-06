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

G = nx.read_gml(r'..\data\karate.gml')
print ("Hello",G)
x1 = nx.eigenvector_centrality(G)
x2 = nx.closeness_centrality(G)
x3 = nx.betweenness_centrality(G)
x4 = nx.degree_centrality(G)
x5 = nx.katz_centrality(G)
print(len(x1)," ",len(x2)," ",len(x3)," ",len(x4)," ",len(x5))
print(x1,x2,x3,x4,x5)

#nx.draw_networkx(G)
#plt.show()
start = time.time()
k_val = []
apl_val = []
raw_apl = []
original_centrality_val = []
noise_centrality_val = []
number_runs = int(input("Enter number of iterations: \n"))
p = 0

#G = nx.convert_node_labels_to_integers(H, label_attribute = 'author_name')
add = 0
lol = 0
max_order = 2
for g in nx.connected_component_subgraphs(G):
    if g.order() > 2:
        add = add + nx.average_shortest_path_length(g)
        lol = lol + 1
        if g.order() > max_order:
            max_order = g.order()
            original_center = nx.center(g)
#print add / lol, lol
# initial_apl = add/lol
if nx.is_connected(G):
    initial_apl = nx.average_shortest_path_length(G)

print("Initial apl is: ",initial_apl)

helpers.plot_graph(G)

original_cc = nx.average_clustering(G)
while p < number_runs:
    G = nx.read_gml(r'..\data\karate.gml')
    for node in G.nodes:
        G.add_node(node, label = node[0], degree = G.degree[node])
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
    k = int(input("Enter the value of k \n"))                                           ## Taking input for K-Anonymity
    #alpha = input("Enter the value of alpha \n")                                   ## Taking input for Alpha
    #cent_measure = raw_input("Enter the centrality measure : \n")
    alpha = 0.25
    l = int(input("Enter the value of l \n"))
    k_val.append(k)
    if 1 == 1:
        degc = {}
        degc = nx.eigenvector_centrality(G)
        degc = sorted(degc.items(), key = itemgetter(1), reverse = True)
        target = G.node[degc[0][0]]['degree']                                      ## For the first time, setting target degree
        labels_present = []
        targets_present = []
        temp_labels_present = []
        count = 1                                                                  ## Count denotes number of nodes in each equivalence group
        c_var = 3
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
        dec_degree = []
        inc_degree = []
        #print targets_present
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
            #print G.node[val]['target_degree'], G.node[val]['degree']
    ## SETTING DEGREE OF NOISE NODES
        # diff = []
        # for n in G.nodes():
        #     if G.node[n]['target_degree'] == 0 and G.degree(n) not in targets_present:
        #         neig = nx.single_source_shortest_path_length(G,n,cutoff = 3)
        #         if G.degree(n) % 2 == 0:
        #             for m in targets_present:
        #                 if m % 2 == 0 and m > G.degree(n):
        #                     diff.append(m)
        #             for k,v in neigh.items():
        #                 if m % 2 != 0 and m > G.degree(n):
        #                     if v > 1 and G.degree(k) not in targets_present and G.degree(n) != G.degree(min(diff)):
        #                         G.add_edge(n,k)
        #                         G.node[n]['degree'] = G.node[n]['degree'] + 1
        #                         G.node[k]['degree'] = G.node[k]['degree'] + 1
        #                     # print (G.node[n]['degree'], G.degree(n))
        #         else:
        #             for m in targets_present:
        #                 if m % 2 != 0 and m > G.degree(n):
        #                     diff.append(m)
        #             for k,v in neigh.items():
        #                 if len(diff) > 0:
        #                     if v > 1 and G.degree(k) not in targets_present and G.degree(n) != G.degree(min(diff)):
        #                         G.add_edge(n,k)
        #                         G.node[n]['degree'] = G.node[n]['degree'] + 1
        #                         G.node[k]['degree'] = G.node[k]['degree'] + 1
                            # print (G.node[n]['degree'], G.degree(n))
    #for n in G.nodes():
        #if G.node[n]['degree'] != G.degree(n):
    #    print G.node[n]['target_degree'], G.degree(n), G.node[n]['degree']
    end = time.time()
    print (end - start)
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
    #print G.order()
    add = 0
    lol = 0
    max_noise_order = 2
    for g in nx.connected_component_subgraphs(G):
        if g.order() > 2:
            add = add + nx.average_shortest_path_length(g)
            lol = lol + 1
            if g.order() > max_noise_order:
                max_noise_order = g.order()
                noise_center = nx.center(g)
            #print g.order(), nx.average_shortest_path_length(g)
    num_of_nodes = G.order()
    apl_val.append(add/lol)
    #apl = (2/(num_of_nodes * (num_of_nodes - 1))) * add
    #apl = (2 / (lol * (lol - 1))) * add
    # print (add / lol, G.order() - 1589, res / cnt)
    #plt.subplot(121)
    #nx.draw(G, node_color = color_map)
    #plt.show()
    p = p + 1
    raw_apl.append(initial_apl)
    original_centrality_val.append(res_original_nodes / cnt_original_nodes)
    noise_centrality_val.append(res / cnt)
    noise_cc = nx.average_clustering(G)
    #print original_center, noise_center
    # print (original_cc, noise_cc)
# print (k_val, apl_val)
l_5 = plt.plot(k_val[0:4], apl_val[0:4], label = 'l = 5', marker = '*')
l_10 = plt.plot(k_val[4:], apl_val[4:], label = 'l = 10', marker = '+')
raw_graph = plt.plot(k_val, raw_apl, label = 'Raw Graph')
plt.xlabel('Values of K')
plt.ylabel('Average Path Length')
plt.legend()
plt.show()

# print (original_centrality_val, noise_centrality_val)
l_5 = plt.plot(k_val[0:4], noise_centrality_val[0:4], label = 'l = 5', marker = '*')
l_10 = plt.plot(k_val[4:], noise_centrality_val[4:], label = 'l = 10', marker = '+')
raw_graph = plt.plot(k_val, original_centrality_val, label = 'Raw Graph')
plt.xlabel('Values of K')
plt.ylabel('Social Importance')
plt.legend()
plt.show()

helpers.plot_graph(G)
