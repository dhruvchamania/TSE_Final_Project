import networkx as nx
from matplotlib import pyplot as plt

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



print("\n\nThe graph is: ")
print(graph)

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


#G = nx.read_gml('netscience.gml')
plot_graph(G)
nx.write_gml(G, "temp.gml")