# select multi-hop path using dokg entity or relation

import pickle
import pandas as pd
import copy
import re
import tqdm

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

dokg_entity_path = "/home/yujin/dot/preprocess_DoKG/data/multi_di/entity_vocab.pkl"
dokg_relation_path = "/home/yujin/dot/preprocess_DoKG/data/multi_di/relation_vocab.pkl"
cnpt_entity_path = "/home/yujin/dot/learning-generator/data/conceptnet/entity_vocab.pkl"

with open(dokg_entity_path, 'rb') as handle:
    entities = pickle.load(handle)

with open(cnpt_entity_path, 'rb') as handle:
    cnpt_entities = pickle.load(handle)

with open(dokg_relation_path, 'rb') as handle:
    relations = pickle.load(handle)

# get list of entities and relations

entities = entities['i2e']
entities = [convert(entity) for entity in entities]
print("origin entities",len(entities))

### if you want to remove duplication activate below code
# except conceptNet duplication
cnpt_entities = cnpt_entities['i2e']
duplicated_entities = [convert(entity) for entity in entities if(convert(entity)) in cnpt_entities]
entities = [convert(entity) for entity in entities if(convert(entity)) not in cnpt_entities]
print("duplicated_entities", duplicated_entities)
print("entities removed duplication",len(entities))

relations = relations['i2r']

path_all_path="/home/yujin/dot/learning-generator/data/sample_path_inte/sample_path.txt"
save_path = "/home/yujin/dot/learning-generator/data/sample_path_inte/sample_path_dokg_only_expt_cnpt.txt"

with open(path_all_path, 'r') as fw:
    path_all = fw.readlines()

dokg_triple_num = 0
with open(save_path, 'w') as sf:
    for line in tqdm.tqdm(path_all):
        flag = False
        line = line.replace("\n", "")
        items = line.split('\t')
        for item in items:
            item_idx = items.index(item)

            if item_idx % 2 == 0 and item in entities:
                flag = True
                items[item_idx] = "".join([item, "*"])

            elif item_idx % 2 == 1 and item in relations:
                flag = True
                items[item_idx] = "".join([item, "**"])

        if flag:
            new_line = "\t".join(items)
            new_line += "\n"
            sf.write(new_line)
            dokg_triple_num += 1
    
print("dokg_triple_num / total_triple_num : {} / {} ".format(dokg_triple_num,len(path_all)))
print("Finish")

# print(len(lines))

# print(lines[-1])