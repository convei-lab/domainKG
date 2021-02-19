import requests
obj = requests.get('http://api.conceptnet.io/c/en/baby').json()
# obj.keys()
# dict_keys(['view', '@context', '@id', 'edges'])

# len(obj['edges'])
# 20

print(len(obj['edges']))

print(obj['edges'][0].keys())
# dict_keys(['@id', '@type', 'dataset', 'end', 'license', 'rel', 'sources', 'start', 'surfaceText', 'weight'])

for edge in obj['edges']:
    entity = edge['end']['label']
    rel = edge['rel']['label']
    print(entity, rel)