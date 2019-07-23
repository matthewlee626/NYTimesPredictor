import csv
import json

counter = 0
with open('unique_isbn_v2.json', mode='r') as jsonList:
    with open('no.json', mode='w') as output:
        isbnInfo = [line for line in jsonList]
        for entry in isbnInfo:
            entryloaded = json.loads(entry)
            keys = list(entryloaded.keys())
            if len(keys) > 0:
                json.dump(entryloaded, output)
                output.write('\n')
                counter += 1
                print(counter)
