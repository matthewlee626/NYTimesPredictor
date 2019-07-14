import json
import csv
import requests


fiction_input = open('fiction.csv', 'r')
nonfiction_input = open('nonfiction.csv', 'r')
fiction_reader = csv.reader(fiction_input, delimiter=',')
nonfiction_reader = csv.reader(nonfiction_input, delimiter=',')


def csv_to_json(reader):
    isbnInfo = []
    line_count = 0
    requestcount = 0

    for row in reader:
        if line_count == 0:
            line_count += 1

        else:
            for i in range(1, 21):
                print("requesting json " + str(requestcount))
                requestcount += 1
                r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' + row[i] + '&format=json&jscmd=data')
                if len(r.json()) != 0:
                    isbnInfo.append(json.dumps(r.json()))
            line_count += 1
    return isbnInfo


with open('bookIBSNInfoCSV.csv', mode='w', newline='') as output:
    masterList = []
    masterList.extend(csv_to_json(fiction_reader))
    masterList.extend(csv_to_json(nonfiction_reader))

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

fiction_input.close()
nonfiction_input.close()