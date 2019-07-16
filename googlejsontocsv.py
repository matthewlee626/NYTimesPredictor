import json
import csv
import requests

# using isbnData.json

START = 0
END = 2505

def getISBNs():
    with open('listOfMissingDatesISBNs.csv', 'r') as csvList:
        reader = csv.reader(csvList, delimiter=',')
        isbnInfo = []
        for line in reader:
            isbnInfo.extend([i for i in line])
        #print(isbnInfo)
        return isbnInfo


def getjson():
    PATHS = ["0150.json", "0300.json", "0450.json", "0600.json", "0750.json", "0900.json", "1000.json", "2000.json", "2170.json", "2340.json", "2505.json"]
    isbnInfo = []
    for i in range(len(PATHS)):
        jsonList = open(PATHS[i], 'r')
        isbnInfo.extend([line for line in jsonList if json.loads(line)['totalItems'] != 0])   # converting json into a list, removing the empty jsons
    return isbnInfo



with open('publishDates.csv', mode='w', newline='', encoding="utf-8") as output:
    masterList = getjson()

    ISBNs = getISBNs()

    csvwriter = csv.writer(output)

    writecount = 0

    header = ['ISBN', 'Publish Date', 'Season', 'Season (int)']  # values we need

    csvwriter.writerow(header)

    index = START

    haveDates = 0
    for jsonLine in masterList:
        j = json.loads(jsonLine) # convert a string value into its corresponding json
        #print(j)


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
        season_date = 0

        if len(mPublishDate) == 10:
            haveDates += 1
            month = int(mPublishDate[5:7])
            if month <= 2 or month == 12:
                season = "Winter"
                season_date = 0
            elif 3 <= month <= 5:
                season = "Spring"
                season_date = 1
            elif 6 <= month <= 8:
                season = "Summer"
                season_date = 2
            elif 9 <= month <= 11:
                season = "Autumn"
                season_date = 3
        else:
            season = "Unknown"

        values = [masterISBN, mPublishDate, season, season_date]

        if len(mPublishDate) == 10:
            print("writing csv line " + str(writecount))
            writecount += 1
            # testing purposes
            csvwriter.writerow(values)

    print(haveDates)
