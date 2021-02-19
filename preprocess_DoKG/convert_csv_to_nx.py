# convert csv file into nx file
import argparse
import pandas as pd
import pickle
import os
import networkx as nx
import re

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# convert uri to entity
def refine_txt(text, rel):
    # delete "" in text
    text = text.replace('"','')
    text = text.replace(" ",'')
    if '#' in text:
        text = text.split('#')[-1]

    if rel == 'rel':
        text = text.lower()
    elif rel == 'reverse_rel':
        text = '_' + text.lower()
    else:
        text = convert(text)
    
    return text

def refine_triples(triples):
    new_df = pd.DataFrame(columns=['ent_h','rel','ent_t'])

    for index, row in triples.iterrows():
        new_row = {'ent_h':refine_txt(row['class'], 'ent'), 'rel':refine_txt(row['relations'], 'rel'), 'ent_t':refine_txt(row['value'], 'ent')}
        reverse_new_row = {'ent_h':refine_txt(row['value'], 'ent'), 'rel':refine_txt(row['relations'], 'reverse_rel'), 'ent_t':refine_txt(row['class'], 'ent')}

        new_df = new_df.append(new_row, ignore_index=True)
        new_df = new_df.append(reverse_new_row, ignore_index=True)


    return new_df

def generate_entity_pkl(new_df, save_dir):
    # create entity_vocab.pkl
    entity_vocab = set()

    for index, row in new_df.iterrows():
        entity_vocab.add(row['ent_h'])
        entity_vocab.add(row['ent_t'])

    # convert to list
    entity_vocab = list(entity_vocab)
    entity_dict = {'e2i': {}, 'i2e':[]}

    for idx, item in enumerate(entity_vocab):
        entity_dict['e2i'][item] = idx
        entity_dict['i2e'].append(item)

    # save into pickle
    save_path = os.path.join(save_dir, 'entity_vocab.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(entity_dict, f, pickle.DEFAULT_PROTOCOL)

    print("{} entities are saved in {}.".format(len(entity_dict['i2e']), save_path))

    return entity_dict

def generate_relation_pkl(new_df, save_dir):
    # create relation_vocab.pkl
    relation_vocab = set()

    for index, row in new_df.iterrows():
        relation_vocab.add(row['rel'])

    # convert to list
    relation_vocab = list(relation_vocab)
    relation_dict = {'r2i': {}, 'i2r':[]}

    for idx, item in enumerate(relation_vocab):
        relation_dict['r2i'][item] = idx
        relation_dict['i2r'].append(item)

    # save into pickle
    save_path = os.path.join(save_dir, 'relation_vocab.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(relation_dict, f, pickle.DEFAULT_PROTOCOL)

    print("{} relations are saved in {}.".format(len(relation_dict['i2r']), save_path))

    return relation_dict

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

def generate_graph(save_dir, entity_dict, relation_dict, new_df, graph_type):
    graph_save_path = os.path.join(save_dir,'baby_domain_graph.nx')

    if (graph_type == 'Di'):
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

    elif (graph_type == 'MultiDi'):
        G = nx.MultiDiGraph()
        # add_node
        G.add_nodes_from(entity_dict['e2i'].values())
        for idx, path in new_df.iterrows():
            ent_h_node = entity_dict['e2i'][path['ent_h']]
            ent_t_node = entity_dict['e2i'][path['ent_t']]
            rel = relation_dict['r2i'][path['rel']]
            # existing path info
            if G.has_edge(ent_h_node, ent_t_node):
                if rel not in [ r['rel'] for r in G[ent_h_node][ent_t_node].values()]:
                    G.add_edges_from([(ent_h_node, ent_t_node, dict(rel=rel))])
            else:
                G.add_edges_from([(ent_h_node, ent_t_node, dict(rel=rel))])

    print(nx.info(G))
    nx.write_gpickle(G, graph_save_path)

    print("Graph is saved in {}".format(graph_save_path))

def main():
    parser = argparse.ArgumentParser(description='Set the file path')
    parser.add_argument('--csv_path', type = str, default =None, help='csv file path')
    parser.add_argument('--head_ent_col_name', type = str, default ='class', help='column name of the head entity in csv file')
    parser.add_argument('--tail_ent_col_name', type = str, default ='value', help='column name of the tail entity in csv file')
    parser.add_argument('--relation_col_name', type = str, default ='relations', help='column name of the head entity in csv file')
    parser.add_argument('--save_dir', type = str, default =None, help='directory path for saving files')
    parser.add_argument('--graph_type', type = str, default ='MultiDi', help='MultiDi or Di')


    args = parser.parse_args()

    # Load triples csv file
    triples = pd.read_csv(args.csv_path) 
    print("The number of triples : {}".format(triples.shape[0]))

    # Path check
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    # Refine the triples
    triples = refine_triples(triples)

    # Generate pickle files
    entity_dict = generate_entity_pkl(triples, args.save_dir)
    relation_dict = generate_relation_pkl(triples, args.save_dir)
    generate_relation_freq_pkl(triples, args.save_dir, relation_dict) 

    # Generate graph
    generate_graph(args.save_dir, entity_dict, relation_dict, triples, args.graph_type)
    
    print("Finish.")


if __name__ == '__main__':
    main()