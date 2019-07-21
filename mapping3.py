import json
import csv
import requests
import time

# using isbnData.json
# getting google books api data

def getISBNs():
    with open('listOfMissingDatesISBNs.csv', 'r') as csvList:
        reader = csv.reader(csvList, delimiter=',')
        isbnInfo = []
        for line in reader:
            isbnInfo.extend([i for i in line])
        print(isbnInfo)
        return isbnInfo

#retrieving data
with open('googleBooksAPIData.json', mode='w', newline='', encoding="utf-8") as output:

    ISBNs = getISBNs()

    print("beg")
    counter = 0
    for masterISBN in ISBNs[1000:2000]:
        print(counter)
        counter += 1
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + masterISBN)
        json.dump(r.json(), output)
        output.write("\n")
        time.sleep(30)
    print("end")
