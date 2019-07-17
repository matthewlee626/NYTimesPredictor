import csv

SEARCH_COUNTER = 0
SEARCH_TIMES = 0


def getTitleISBN():
    with open('isbnToInfo.csv', mode='r', encoding='utf-8') as inputs:
        reader = csv.reader(inputs, delimiter=',')
        isbnList = []
        titleList = []
        line_count = 0
        for line in reader:
            if line_count == 0:
                line_count += 1
            else:
                isbnList.append(line[0])
                titleList.append(line[4])
        return isbnList, titleList


def getFirstDate(isbn):
    #print(isbn)
    global SEARCH_COUNTER
    global SEARCH_TIMES
    SEARCH_TIMES += 1
    #print(SEARCH_TIMES)
    with open('fiction.csv', mode='r', encoding='utf-8') as fiction:
        with open('nonfiction.csv', mode='r', encoding='utf-8') as nonfiction:
            fictionreader = csv.reader(fiction, delimiter=',')
            nonfictionreader = csv.reader(nonfiction, delimiter=',')
            for line in fictionreader:
                for j in line:
                    #print(SEARCH_COUNTER)
                    SEARCH_COUNTER += 1
                    if j == isbn:
                        print("found")
                        return line[0]
            for line2 in nonfictionreader:
                for k in line2:
                    #print(SEARCH_COUNTER)
                    SEARCH_COUNTER += 1
                    if k == isbn:
                        print("found")
                        return line2[0]
    return "Not Found"


isbnInfo, titleInfo = getTitleISBN()

publishDateInfo = []

for l in isbnInfo:
    publishDateInfo.append(getFirstDate(l))

print(SEARCH_COUNTER)

with open('titleISBNdate.csv', mode='w', encoding='utf-8', newline='') as result:
    writer = csv.writer(result)
    header = ['ISBN', "Title", 'FirstDate']
    writer.writerow(header)
    for i in range(len(isbnInfo)):
        writer.writerow([isbnInfo[i], titleInfo[i], publishDateInfo[i]])

