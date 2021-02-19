import networkx as nx
import os
import pickle
import pandas as pd

cnpt_path = "/home/yujin/dot/learning-generator/data/conceptnet"

# load cnpt
cnpt_nx_file = os.path.join(cnpt_path, 'conceptnet_graph.nx')
cnpt = nx.read_gpickle(cnpt_nx_file)

# get input
user_input = input("start entity : ")

entity_path = os.path.join(cnpt_path, 'entity_vocab.pkl')
relation_path = os.path.join(cnpt_path, 'relation_vocab.pkl')

with open(entity_path, 'rb') as fin:
    entities = pickle.load(fin)

with open(relation_path, 'rb') as fin:
    relations = pickle.load(fin)

# search entity_idx
c_ent = entities['e2i'][user_input]

all_path = cnpt[c_ent]
path_df = pd.DataFrame(columns=['rel', 'end_entity'])

for key, val in all_path.items():
    rel = relations['i2r'][val[0]['rel']]
    end_ent = entities['i2e'][key]
    path_df = path_df.append({'rel': rel, 'end_entity': end_ent}, ignore_index=True)
    print(rel, end_ent)

csv_path = os.path.join('/home/yujin/dot/conceptnet', '{}.csv'.format(user_input))
path_df.to_csv(csv_path)

print("finish")