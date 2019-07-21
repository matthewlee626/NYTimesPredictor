import json
import csv
import requests

# using isbnData.json

def getjson():
    jsonList = open('isbnData.json', 'r')
    isbnInfo = [line for line in jsonList if len(json.loads(line)) != 0]  # converting isbnData.json into a list, removing the empty jsons
    return isbnInfo


with open('bookIBSNInfoCSV.csv', mode='w', newline='', encoding="utf-8") as output:
    masterList = getjson()

    csvwriter = csv.writer(output)

    writecount = 0

    header = ['ISBN', 'Author', 'Publisher', 'Publish Date']  # values we need

    csvwriter.writerow(header)

    for jsonLine in masterList:
        j = json.loads(jsonLine)  # convert a string value into its corresponding json

        print("writing csv line " + str(writecount))
        writecount += 1
        # testing purposes

        masterISBN = list(j.keys())[0]  # returns value in format "ISBN:XXXXXXXXX'

        mMasterISBN = ""
        mPublisher = ""
        mPublishDate = ""
        mAuthor = ""

        if masterISBN != "":  # should'nt ever need this, just a backup case
            mMasterISBN = masterISBN[5:]
        else:
            mmasterISBN = "0"

        # if x in y simply checks whether x exists inside y, thus allowing access to it
        # if x doesn't exist, a filler value is put into place

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

        # mapping values
        values = [mMasterISBN, mPublisher, mPublishDate, mAuthor]

        csvwriter.writerow(values)
