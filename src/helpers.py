from __future__ import division
import networkx as nx
import collections
import random
import string

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