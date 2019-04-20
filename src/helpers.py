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
