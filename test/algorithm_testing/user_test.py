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

check=False
try:
    a = int(input("Enter the method that you want to test on 1. edge editing, 2. noise node addition\n"))
    if a==1 or a==2:
        check=True
except:
    a=10
while not check:
    try:
        a = int(input("Please enter a valid input: 1. edge editing, 2. noise node addition\n"))
        if a == 1 or a == 2:
            check = True
    except:
        a=10


try:
    i = int(input("Enter 1 for synthetic graph, otherwise running for existing dataset\n"))
except:
    i=None



#i = int(input("Enter 1 for synthetic graph, otherwise running for existing dataset\n"))


if i == 1:
    graph=[]
    G=nx.Graph()

    print("\n\nBuild your graph")
    print("Enter minimum 10 number of nodes and edges for graph.\n")
    print("STEP 1:\tAdd nodes in the following format: node_number label:")
    print("Press enter without adding any node start adding edges.\n")
    n = str(input("Enter node : "))

    while n!='':
        q=n.split(" ")
        if len(q)==2:
            node = q[0]
            label = q[1]
            G.add_node(node, label=label)
            G.node[node]['label']=label
            n = str(input("Enter the next node : "))
        else:
            print("\nInvalid format! Please enter the node in this format: node_number label\nPress enter without adding any node to start adding edges.\n")
            n = str(input("Enter the next node : "))

    print("\nSTEP 2:\tAdd edges in the following format: node1\tnode2")
    print("Press enter without adding any edge to stop adding edges.\n\n")
    inp = str(input("Enter the edge: \n"))
    while inp != '':
        q = inp.split(" ")
        if len(q)==2:
            n1 = q[0]
            n2 = q[1]
            graph.append(q)
            G.add_edge(n1, n2)  # default edge data=1
            inp = str(input("Enter the next edge: \n"))

        else:
            print("\nInvalid format! Please enter the edge in this format: node1\tnode2\nPress enter without adding any edge to stop adding edges.\n")
            n = str(input("Enter the next edge : "))

    nx.write_gml(G, "temp.gml")
    path = r'temp.gml'
    print("Graph created!! ")
    print("Path: "+path)

else:

    check = False
    try:
        j = int(input("\n\nEnter the dataset you want to test on, 1: Karate(40 approx nodes), 2: netscience(1400 approx nodes), 3: netscience2(1500 nodes)\n"))
        if j == 1 or j == 2 or j==3:
            check = True
    except:
        j = 10
    while not check:
        try:
            j = int(input("Please enter a valid input: 1: Karate(40 approx nodes), 2: netscience(1400 approx nodes), 3: netscience2(1500 nodes)\n"))
            if j == 1 or j == 2 or j == 3:
                check = True
        except:
            j = 10

    if j == 1:
        path = r'..\..\data\karate.gml'
    elif j == 2:
        path = r'..\..\data\netscience.gml'
    elif j == 3:
        path = r'..\..\data\as-22july06.gml'
    else:
        print("Using default karate")
        path = r'..\..\data\karate.gml'

check = False
try:
    k = int(input("\nEnter the centrality you want test for, 1 for eigen, 2 for closness, 3 for betweeness, 4 for degree, 5 for katz\n"))
    if k in range(1,6):
        check = True
except:
    k = 10
while not check:
    try:
        k = int(input("Please enter a valid input: 1 for eigen, 2 for closness, 3 for betweeness, 4 for degree, 5 for katz\n"))
        if k in range(1,6):
            check = True
    except:
        k=10

#k = int(input("Enter the centrality you want test for, 1 for eigen, 2 for closness, 3 for betweeness, 4 for degree, 5 for katz.\n"))
l = int(input("Enter the type of privacy measure you want to test on 1 for only k, 2 for k&l and 3 for all the privacy measure. Default is only k\n"))
if l is not 1 or l is not 2 or l is not 3:
	l = 1
check = False
try:
    K = int(input("\nEnter the value of k\n"))
    check=True
except:
    K = 1
while not check:
    try:
        K = int(input("Enter the value of k\n"))
        check = True
    except:
        K=1

#K = int(input("Enter the value of k\n"))

check = False
try:
    L = int(input("Enter the value of l\n"))
    check=True
except:
    L = 1
while not check:
    try:
        L = int(input("Enter the value of l\n"))
        check = True
    except:
        L=1

#L = int(input("Enter the value of l\n"))


if a == 1:
    G1,G2,X,Y,E = edge_editing.edge_editing(K,L,l,k,1,path)
    helpers.centrality_top_20_compare(G1,G2)
else:
    G1,G2,X,Y,E = noise_node_addition.noise_node_addition(K,L,l,k,1,path)
    helpers.centrality_top_20_compare(G1,G2)
    
helpers.plot_graph2(G1,G2,helpers.get_title(l-1,k-1))

