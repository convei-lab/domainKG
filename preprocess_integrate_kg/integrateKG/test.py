import networkx as nx

G = nx.DiGraph()

nodes_1 = [1,2,3]
nodes_2 = [2,3,4]

G.add_nodes_from(nodes_1)
print(nx.info(G))


G.add_nodes_from(nodes_2)
print(nx.info(G))