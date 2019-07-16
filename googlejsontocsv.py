import json
import csv
import requests

# using isbnData.json

START = 1000
END = 2000

def getISBNs():
    with open('listOfMissingDatesISBNs.csv', 'r') as csvList:
        reader = csv.reader(csvList, delimiter=',')
        isbnInfo = []
        for line in reader:
            isbnInfo.extend([i for i in line])
        #print(isbnInfo)
        return isbnInfo


def getjson():
    PATH = "C:\\Users\\matth\\Desktop\\NYTimesPredictor\\GoogleJSON\\googleBooksAPIData2000.json"
    jsonList = open(PATH, 'r')
    isbnInfo = [line for line in jsonList if json.loads(line)['totalItems'] != 0]  # converting json into a list, removing the empty jsons
    return isbnInfo



with open('publishDates.csv', mode='w', newline='', encoding="utf-8") as output:
    masterList = getjson()

    ISBNs = getISBNs()

    csvwriter = csv.writer(output)

    writecount = 0

    header = ['ISBN', 'Publish Date']  # values we need

    csvwriter.writerow(header)

    index = START

    haveDates = 0
    for jsonLine in masterList:
        j = json.loads(jsonLine) # convert a string value into its corresponding json
        #print(j)
        print("writing csv line " + str(writecount))
        writecount += 1
        # testing purposes

        masterISBN = ISBNs[index]
        index += 1

        mPublishDate = ""


        # if x in y simply checks whether x exists inside y, thus allowing access to it
        # if x doesn't exist, a filler value is put into place

        if "publishedDate" in j['items'][0]['volumeInfo']:
            mPublishDate = j['items'][0]['volumeInfo']['publishedDate']
        else:
            mPublishDate = "Date 0"

        season = ""

        if len(mPublishDate) == 10:
            haveDates += 1
            month = int(mPublishDate[5:7])
            if month <= 2 or month == 12:
                season = "Winter"
            elif 3 <= month <= 5:
                season = "Spring"
            elif 6 <= month <= 8:
                season = "Summer"
            elif 9 <= month <= 11:
                season = "Autumn"
        else:
            season = "Unknown"

        values = [masterISBN, mPublishDate, season]

        csvwriter.writerow(values)

    print(haveDates)
