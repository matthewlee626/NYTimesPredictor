import json
import csv
import requests

# using isbnData.json

def getjson():
    jsonList = open('isbnData.json', 'r')
    isbnInfo = [line for line in jsonList if len(json.loads(line)) != 0]
    print(isbnInfo)
    return isbnInfo


with open('bookIBSNInfoCSV.csv', mode='w', newline='', encoding="utf-8") as output:
    masterList = getjson()

    csvwriter = csv.writer(output)

    count = 0
    writecount = 0

    header = ['ISBN', 'Author', 'Publisher', 'Publish Date']
    csvwriter.writerow(header)

    for jsonLine in masterList:
        j = json.loads(jsonLine)

        print("writing csv line " + str(writecount))
        writecount += 1

        masterISBN = list(j.keys())[0]

        mMasterISBN = ""
        mPublisher = ""
        mPublishDate = ""
        mAuthor = ""

        if masterISBN != "":
            mMasterISBN = masterISBN[5:]
        else:
            mmasterISBN = "0"

        if 'publishers' in j[masterISBN]:
            mPublisher = j[masterISBN]['publishers'][0]['name']
        else:
            mPublisher = "Blank Publisher"

        if 'publish_date' in j[masterISBN]:
            mPublishDate = j[masterISBN]['publish_date']
        else:
            mPublishDate = "Date 0"

        if 'authors' in j[masterISBN]:
            mAuthor = j[masterISBN]['authors'][0]['name']
        else:
            mAuthor = "Some Random Author"

        values = [mMasterISBN, mPublisher, mPublishDate, mAuthor]

        csvwriter.writerow(values)
