# TODO: implement the hasher: ie sum of squared genre frequencies divided by categories normalized
import csv
import json

with open("yes.json", mode='r') as input:
    with open("yes.csv", mode='w') as output:
        isbnInfo = [line for line in input]
        print(isbnInfo)
        for entry in isbnInfo:
            entryloaded = json.loads(entry)
            keys = list(entryloaded.keys())
            print(keys)