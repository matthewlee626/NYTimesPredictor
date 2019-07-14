import json
import csv
import requests
import time

# using isbnData.json
# getting google books api data

def getjson():
    with open('isbnData.json', 'r') as jsonList:
        isbnInfo = [line for line in jsonList if len(json.loads(line)) != 0]
        return isbnInfo


with open('googleBooksAPIData.json', mode='w', newline='', encoding="utf-8") as output:
    jsonData = getjson()

    ISBNs = []


    for jsonLine in jsonData:
        j = json.loads(jsonLine)
        ISBN = list(j.keys())[0][5:]
        ISBNs.append(ISBN)

    print("beg")
    counter = 0
    for masterISBN in ISBNs:
        print(counter)
        counter += 1
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + masterISBN)
        json.dump(r.json(), output)
        output.write("\n")
        time.sleep(30)
    print("end")
