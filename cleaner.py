import json

with open('isbnData.json', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    for p in data:
        print(p)
