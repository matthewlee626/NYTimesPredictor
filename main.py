import json

with open('nyt2.json', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    for p in data:
        print(p['_id'])
        print('')