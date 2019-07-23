import csv
import json

counter = 0
with open('fictionsingle.csv', mode='r') as fiction_input:
    with open('isbnData.json', mode='r') as jsonList:
        with open('yes.json', mode='w') as output:
            isbnInfo = [line for line in jsonList]
            fiction_reader = csv.reader(fiction_input, delimiter=',')
            for row in fiction_reader:
                for entry in isbnInfo:
                    entryloaded = json.loads(entry)
                    keys = list(entryloaded.keys())
                    if len(keys) > 0: # and len(row) > 0:
                        formattedkey = keys[0][5:]
                        if row[0] == formattedkey:
                            json.dump(entryloaded, output)
                            output.write('\n')
                            counter += 1
                            print(counter)