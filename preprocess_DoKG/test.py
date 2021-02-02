import networkx as nx

G = nx.MultiDiGraph()

G.add_nodes_from([0,1,2])

# G[0][1][0]['rel'] = 200
edge_list = []
edge_list.append((0,1, dict(rel=100)))
G.add_edges_from(edge_list)
edge_list = []

if 100 not in [rel['rel'] for rel in G[0][1].values()]:
    edge_list.append((0,1, dict(rel=100)))
    G.add_edges_from(edge_list)

print(G[0])




# # existing path info
# if G.has_edge(ent_h_node, ent_t_node):
#     for key, val in G[ent_h_node][ent_t_node].items():
#         edge_list.append((ent_h_node, ent_t_node, dict(rel=val['rel'])))
#         rel = relation_dict['r2i'][path['rel']]
#     edge_list.append((ent_h_node, ent_t_node, dict(rel=rel)))
#     G.add_edges_from(edge_list)

print(G.edges(data=True))