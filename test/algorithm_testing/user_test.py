#User Test Case

import sys
sys.path.append(r"..\..")
from src import helpers
from src import edge_editing
from src import noise_node_addition
import networkx as nx
import operator
import pandas as pd

G1 = nx.Graph()
G2 = nx.Graph()
X = Y = E = 0


a = int(input("Enter the method that you want to test on 1. edge editing, 2. noise node addition\n"))
i = int(input("Enter 1 for synthetic graph, otherwise running for existing dataset\n"))
if i == 1:
    graph=[]
    G=nx.Graph()

    print("Build a graph\n\n")
    print("Add nodes in the following format: node_number label:")
    n = str(input("Enter node : "))

    while n!='':
        q=n.split(" ")
        node = q[0]
        label = q[1]
        G.add_node(node, label=label)
        G.node[node]['label']=label
        n = str(input("Enter the next node : "))

    print("\nAdd edges in the following format: node1\tnode2")

    inp = str(input("Enter the edge: \n"))
    while inp != '':
        q = inp.split(" ")
        n1 = q[0]
        n2 = q[1]
        graph.append(q)
        G.add_edge(n1, n2)  # default edge data=1
        inp = str(input("Enter the next edge: \n"))
    nx.write_gml(G, "temp.gml")
    path = r'..\..\data\temp.gml'

else:
    j = int(input("Enter the dataset you want to test on, 1: Karate(40 approx nodes), 2: netscience(100 approx nodes), 3: Internet(20000 nodes)\n"))
    if j == 1:
        path = r'..\..\data\karate.gml'
    elif j == 2:
        path = r'..\..\data\netscience.gml'
    elif j == 3:
        path = r'..\..\data\as-22july06.gml'
    else:
        print("Please Enter correct value")

k = int(input("Enter the centrality you want test for, 1 for eigen, 2 for closness, 3 for betweeness, 4 for degree, 5 for katz\n"))
l = int(input("Enter the type of privacy measure you want to test on 1 for  \n"))
K = int(input("Enter the value of k\n"))
L = int(input("Enter the value of l\n")) 
if a == 1:
    G1,G2,X,Y,E = edge_editing.edge_editing(K,L,l,k,1,path)
    helpers.centrality_top_20_compare(G1,G2)
else:
    G1,G2,X,Y,E = noise_node_addition.noise_node_addition(K,L,l,k,1,path)
    helpers.centrality_top_20_compare(G1,G2)
    
helpers.plot_graph2(G1,G2,helpers.get_title(l-1,k-1))

