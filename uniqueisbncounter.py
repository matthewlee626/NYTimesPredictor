import json
import csv
import requests

# using isbnData.json


with open('unique_isbn_v2.json', 'r') as jsonList:
    isbnInfo = [line for line in jsonList if len(json.loads(line)) != 0]
    fullInfo = [line for line in jsonList]
    print(len(fullInfo))
    print(len(isbnInfo))
