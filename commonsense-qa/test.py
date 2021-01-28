def find_relational_paths(cpnet_vocab_path, cpnet_graph_path, grounded_path, output_path, num_processes, use_cache):
    if use_cache and os.path.exists(output_path):
        print(f'using cached relational paths from {output_path}')
        return
    print("hello")

    def get_cpnet_simple(nx_graph):
        cpnet_simple = nx.Graph()
        for u, v, data in nx_graph.edges(data=True):
            w = data['weight'] if 'weight' in data else 1.0
            if cpnet_simple.has_edge(u, v):
                cpnet_simple[u][v]['weight'] += w
            else:
                cpnet_simple.add_edge(u, v, weight=w)
        return cpnet_simple

    global concept2id, id2concept, relation2id, id2relation, cpnet_simple, cpnet
    
    if any(x is None for x in [concept2id, id2concept, relation2id, id2relation]):
        with open(cpnet_vocab_path, 'r', encoding='utf-8') as fin:
            id2concept = [w.strip() for w in fin]
        concept2id = {w: i for i, w in enumerate(id2concept)}
        id2relation = merged_relations.copy()
        id2relation += ['*' + r for r in id2relation]
        relation2id = {r: i for i, r in enumerate(id2relation)}
    if cpnet is None or cpnet_simple is None:
        cpnet = nx.read_gpickle(cpnet_graph_path)
        cpnet_simple = get_cpnet_simple(cpnet)

    print("type of id 2 relation",type(id2relation))
    raise RuntimeError()
    with open(grounded_path, 'r') as fin:
        data = [json.loads(line) for line in fin]
    data = [[item["ac"], item["qc"]] for item in data]

    with Pool(num_processes) as p, open(output_path, 'w') as fout:
        for pfr_qa in tqdm(p.imap(find_relational_paths_qa_pair, data), total=len(data), desc='Finding relational paths'):
            fout.write(json.dumps(pfr_qa) + '\n')

    print(f'paths saved to {output_path}')
    print()



from multiprocessing import cpu_count

cpnet_vocab_path='./data/cpnet/concept.txt'
cpnet_graph_path='./data/cpnet/conceptnet.en.pruned.graph'
nprocs=cpu_count()

test_concepts='./data/csqa/grounded/test.grounded.jsonl'
test_rel_paths='./data/csqa/paths/test.relpath.2hop.jsonl'

use_cache=False


find_relational_paths(cpnet_vocab_path, cpnet_graph_path, test_concepts, test_rel_paths, nprocs, use_cache)