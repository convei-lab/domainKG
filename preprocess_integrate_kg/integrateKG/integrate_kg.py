# convert csv file into nx file
import argparse
import pandas as pd
import pickle
import os
import networkx as nx
import re

# convert uri to entity
def refine_txt(text):
    # delete "" in text
    text = text.replace('"','')
    text = text.replace(" ",'')
    if '#' in text:
        text = text.split('#')[-1]
    return text

def refine_triples(triples):
    new_df = pd.DataFrame(columns=['ent_h','rel','ent_t'])

    for index, row in triples.iterrows():
        new_row = {'ent_h':refine_txt(row['class']), 'rel':refine_txt(row['relations']), 'ent_t':refine_txt(row['value'])}
        new_df = new_df.append(new_row, ignore_index=True)

    return new_df


def generate_relation_freq_pkl(new_df, save_dir, relation_dict):
    # create relation_freq.pkl
    triples_freq = new_df['rel'].value_counts()
    total_triples_num = new_df.shape[0]
    relation_freq = {}
    for idx, item in enumerate(relation_dict['i2r']):
        relation_freq[idx] = triples_freq[item] / total_triples_num

    # save into pickle
    save_path = os.path.join(save_dir, 'relation_freq.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(relation_freq, f, pickle.DEFAULT_PROTOCOL)
    
    print("relation frequency is saved in {}.".format(save_path))

def generate_graph(save_dir, entity_dict, relation_dict, new_df):
    graph_save_path = os.path.join(save_dir,'baby_domain_graph.nx')
    G = nx.DiGraph()

    # add_node
    G.add_nodes_from(entity_dict['e2i'].values())

    for idx, path in new_df.iterrows():
        ent_h_node = entity_dict['e2i'][path['ent_h']]
        ent_t_node = entity_dict['e2i'][path['ent_t']]
        rel = relation_dict['r2i'][path['rel']]
        G.add_edge(ent_h_node, ent_t_node)
        rel_idx = len(G[ent_h_node][ent_t_node])
        G[ent_h_node][ent_t_node][rel_idx] = {'rel': rel}

    print(nx.info(G))
    nx.write_gpickle(G, graph_save_path)

    print("Graph is saved in {}".format(graph_save_path))

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def integrate_entity_pkl(std_kg_path, add_kg_path, save_dir):
    std_kg_ent_path = os.path.join(std_kg_path,"entity_vocab.pkl")
    add_kg_ent_path = os.path.join(add_kg_path,"entity_vocab.pkl")

    with open(std_kg_ent_path, 'rb') as handle:
        std_kg_ents = pickle.load(handle)

    with open(add_kg_ent_path, 'rb') as handle:
        add_kg_ents = pickle.load(handle)

    integrate_entity_dict = {'e2i': {}, 'i2e':[]}

    # load std_kg_ents
    integrate_entity_dict['e2i'] = std_kg_ents['e2i']
    integrate_entity_dict['i2e'] = std_kg_ents['i2e']

    # integrate add_kg_ents
    dup_num = 0
    convert_info_dict = {}
    for index, entity in enumerate(add_kg_ents['i2e']):
        new_entity = convert(entity)
        if new_entity in integrate_entity_dict['i2e']:
            convert_info_dict[index] = integrate_entity_dict['e2i'][new_entity]
            dup_num += 1
        else:
            new_index = len(integrate_entity_dict['i2e'])
            integrate_entity_dict['e2i'][new_entity] = new_index
            integrate_entity_dict['i2e'].append(new_entity)
            convert_info_dict[index]=new_index

    # save into pickle
    save_path = os.path.join(save_dir, 'entity_vocab.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(integrate_entity_dict, f, pickle.DEFAULT_PROTOCOL)

    print("{} entities are duplicated. The total number of integrated kg entityes is {}.".format(dup_num,len(integrate_entity_dict['i2e'])))

    print("{} entities are saved in {}.".format(len(integrate_entity_dict['i2e']), save_path))

    return convert_info_dict

def integrate_relation_pkl(std_kg_path, add_kg_path, save_dir, conv_dict):
    std_kg_rel_path = os.path.join(std_kg_path,"relation_vocab.pkl")
    add_kg_rel_path = os.path.join(add_kg_path,"relation_vocab.pkl")

    with open(std_kg_rel_path, 'rb') as handle:
        std_kg_rels = pickle.load(handle)

    with open(add_kg_rel_path, 'rb') as handle:
        add_kg_rels = pickle.load(handle)

    integrate_relation_dict = {'r2i': {}, 'i2r':[]}

    # load std_kg_rels
    integrate_relation_dict['r2i'] = std_kg_rels['r2i']
    integrate_relation_dict['i2r'] = std_kg_rels['i2r']

    # integrate add_kg_rels
    convert_info_dict = {}
    for index, rel in enumerate(add_kg_rels['i2r']):
        if rel in conv_dict.keys():
            convert_info_dict[index] = integrate_relation_dict['r2i'][conv_dict[rel]]
        else:
            new_index = len(integrate_relation_dict['i2r'])
            integrate_relation_dict['r2i'][rel] = new_index
            integrate_relation_dict['i2r'].append(rel)
            convert_info_dict[index]=new_index
    # save into pickle
    save_path = os.path.join(save_dir, 'relation_vocab.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(integrate_relation_dict, f, pickle.DEFAULT_PROTOCOL)

    print("{} relation are converted. The total number of integrated kg relationes is {}.".format(len(conv_dict),len(integrate_relation_dict['i2r'])))

    print("{} relations are saved in {}.".format(len(integrate_relation_dict['i2r']), save_path))

    return convert_info_dict
    

def integrate_graph(std_kg_path, std_kg_name, add_kg_path, add_kg_name, save_dir, entity_convert_idx_info, relation_convert_idx_info):

    # load std_kg
    std_graph_path = os.path.join(std_kg_path, "{}.nx".format(std_kg_name))
    int_graph = nx.read_gpickle(std_graph_path)

    # load entities and relations
    entity_path = os.path.join(save_dir, "entity_vocab.pkl")
    with open(entity_path, 'rb') as handle:
        entities = pickle.load(handle)

    relation_path = os.path.join(save_dir, "relation_vocab.pkl")
    with open(relation_path, 'rb') as handle:
        relations = pickle.load(handle)

    int_graph.add_nodes_from(entities['e2i'].values())

    # load add_graph edges
    add_graph_path = os.path.join(add_kg_path, "{}.nx".format(add_kg_name))
    add_G = nx.read_gpickle(add_graph_path)

    for n1 in add_G.nodes():
        for n2 in add_G[n1].keys():
            # convert node idx
            st_node = entity_convert_idx_info[n1]
            end_node = entity_convert_idx_info[n2]
            for key, val in add_G[n1][n2].items():
                rel = relation_convert_idx_info[val['rel']]
                if int_graph.has_edge(st_node,end_node):
                    if rel not in [ r['rel'] for r in int_graph[st_node][end_node].values()]:
                        int_graph.add_edges_from([(st_node, end_node, dict(rel=rel))])
                else:
                    int_graph.add_edges_from([(st_node, end_node, dict(rel=rel))])

    graph_save_path = os.path.join(save_dir,'integrate_graph.nx')

    nx.write_gpickle(graph_save_path, graph_save_path)
    print("**add_graph_info**")
    print(nx.info(add_G))
    print("**int_graph_info**")
    print(nx.info(int_graph))
    print("Graph is saved in {}".format(graph_save_path))

def main():
    parser = argparse.ArgumentParser(description='Set the file path')
    parser.add_argument('--std_kg_path', type = str, default =None, help='standard kg directory path')
    parser.add_argument('--std_kg_name', type = str, default =None, help='standard kg name')
    parser.add_argument('--add_kg_path', type = str, default =None, help='additional kg directory path')
    parser.add_argument('--add_kg_name', type = str, default =None, help='additional kg name')
    parser.add_argument('--integrate_list_path', type = str, default =None, help='integrate list file path')
    parser.add_argument('--save_dir', type = str, default =None, help='dir path for output file')

    args = parser.parse_args()

    # Load triples csv file
    items = pd.read_csv(args.integrate_list_path) 
    from_str = items.columns[0]
    to_str = items.columns[1]
    print("the number of integrated items : {}".format(items.shape[0]))

    # Change into dictionary format
    conv_dict = {}
    for idx, row in items.iterrows():
        conv_dict[row[from_str]] = row[to_str]


    # Merge entities
    entity_convert_idx_info = integrate_entity_pkl(args.std_kg_path, args.add_kg_path, args.save_dir)
    relation_convert_idx_info = integrate_relation_pkl(args.std_kg_path, args.add_kg_path, args.save_dir, conv_dict)
    # integrate_relation_freq_pkl(triples, args.save_dir, relation_dict) 

    # Generate graph
    integrate_graph(args.std_kg_path, args.std_kg_name, args.add_kg_path, args.add_kg_name, args.save_dir, entity_convert_idx_info, relation_convert_idx_info)
    
    print("Finish.")


if __name__ == '__main__':
    main()