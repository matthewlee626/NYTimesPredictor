import json
import csv
import requests

# using isbnData.json


def one():
    with open('C:\\Users\\matth\\Desktop\\NYTimesPredictor\\isbnData.json', mode='r', encoding='utf-8') as jsonList:
        fullInfo = [line2 for line2 in jsonList if len(json.loads(line2)) > -1]
        print(len(fullInfo))

def two():
    with open('C:\\Users\\matth\\Desktop\\NYTimesPredictor\\isbnData.json', mode='r', encoding='utf-8') as jsonList2:
        isbnInfo = [line for line in jsonList2 if len(json.loads(line)) != 0]
        print(len(isbnInfo))

one()
two()