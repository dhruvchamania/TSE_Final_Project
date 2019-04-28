# Noise Node for karate.gml dataset
# Dataset for least amount of nodes.

import sys
sys.path.append(r"..\..")
from src import helpers
from src import edge_editing
import networkx as nx

G1 = nx.Graph()
G2 = nx.Graph()
g = []
x = []
y = [] 

k = int(input("Enter the value of k \n"))
l = int(input("Enter the value of l \n"))
X = Y = Ya = 0
for i in range(0,3):
    for j in range(0,4):
        print(i+1,j+1)
        G1,G2,X,Y = edge_editing.edge_editing(k,l,i+1,j+1,r'..\..\data\karate.gml')
        print("Number of nodes in original graph: ",len(G1.nodes),"Number of nodes in anonymised graph: ", len(G2.nodes))
        print(len(G1.edges), len(G2.edges))
        Y = Y/(1024*1024)
        print(X,Y)
        y.append(Y)
        x.append(X)
        g.append(G2)

print("Number of nodes in original graph: ",len(G1.nodes),"Number of nodes in anonymised graph: ", len(G2.nodes))
print(len(G1.edges), len(G2.edges))
print("Time Taken in sec",x)
print("Memory Consumed in MB",y)
helpers.plot_graph(G1)
helpers.plot_graph(G2)