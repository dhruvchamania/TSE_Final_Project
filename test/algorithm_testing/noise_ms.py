# Testing for multiple labelled dataset using Noise Node Addition technique.

import sys
sys.path.append(r"..\..")
from src import helpers_ms
from src import noise_node_addition_ms
import networkx as nx
import operator
import pandas as pd

G1 = nx.Graph()
G2 = nx.Graph()
mp = {}
k = int(input("Enter the value of k \n"))
l = int(input("Enter the value of l \n"))
X = Y = E = 0
title = []
g = []
for i in range(0,3):
    for j in range(0,5):
        mp[helpers_ms.get_title(i,j)] = []
        #print(i+1,j+1)
        G1,G2,X,Y,E = noise_node_addition_ms.noise_node_addition(k,l,i+1,j+1,1,r'..\..\data\karate.gml')
        Y = Y/(1024*1024)
        #print(X,Y)
        g.append(G2)
        title.append(helpers_ms.get_title(i,j))
        mp[helpers_ms.get_title(i,j)].append(G2)
        mp[helpers_ms.get_title(i,j)].append(X)
        mp[helpers_ms.get_title(i,j)].append(Y)
        mp[helpers_ms.get_title(i,j)].append(E)
        mp[helpers_ms.get_title(i,j)].append(abs(len(G2.edges) - len(G1.edges)))
        mp[helpers_ms.get_title(i,j)].append(helpers_ms.centrality_top_20_compare(G1,G2))

sorted_time = sorted(mp.items(), key = lambda x: x[1][1])
time = {}
for i in range(len(sorted_time)):
    time[sorted_time[i][0]] = i + 1
sorted_memory = sorted(mp.items(), key = lambda x: x[1][2])
memory = {}
for i in range(len(sorted_time)):
    memory[sorted_memory[i][0]] = i + 1
sorted_error = sorted(mp.items(), key = lambda x: x[1][3])
error = {}
for i in range(len(sorted_time)):
    error[sorted_error[i][0]] = i + 1
sorted_nodes = sorted(mp.items(), key = lambda x: x[1][4])
diff_nodes = {}
for i in range(len(sorted_time)):
    diff_nodes[sorted_nodes[i][0]] = i + 1
sorted_compare = sorted(mp.items(), key = lambda x: x[1][5],reverse= True)
compare_nodes = {}
for i in range(len(sorted_time)):
    compare_nodes[sorted_nodes[i][0]] = i + 1
rank = []
for i in title:
    rank.append((i,time[i] + memory[i] + error[i] + diff_nodes[i] + compare_nodes[i]))
rank = sorted(rank, key = lambda x:x[1])
#print(rank)
print('\n')
print("Number of nodes in karate dataset: ",len(G1.nodes),"Number of edges in karate science dataset: ", len(G2.edges))
print('\n')
#print(len(G1.edges), len(G2.edges))
#print(mp)
#helpers.plot_graph(G1)
#helpers.plot_graph(G2)
x = pd.DataFrame(mp)
#print(x)
x = x.T
Frame=pd.DataFrame(x.values, columns = ["(Name)","(Time Taken in sec)", "(Memory Consumed in MB)", "(Error in path length)", "(Node difference)","(Top 20 Centrality)"])
count = 0
for i in range(0,3):
        for j in range(0,5):
                Frame['(Name)'][count] = helpers_ms.get_title(i,j)
                count+=1
print(Frame)
print('\n')
print("Sorted according to Rank (A metric of all the data combined)")
for i in rank:
    print(i[0])
Frame.to_csv('noise_ms.csv',sep='\t')


#for i, graph in enumerate(g):
#       helpers.plot_graph2(G1,graph,title[i])
for i in range(0,1):
        helpers_ms.plot_graph2(G1,g[i],title[i])
