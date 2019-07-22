import csv

SEARCH_COUNTER = 0
SEARCH_TIMES = 0


with open('fictionsingle.csv', mode='r', encoding='utf-8') as input:
    with open('titleISBNdate.csv', mode='r', encoding='utf-8') as base:
        with open('titleISBNdateFiction.csv', mode='w', encoding='utf-8', newline='') as result:
            reader = csv.reader(input, delimiter = ',')
            isbnInfo = []
            for line in reader:
                isbnInfo.extend([i for i in line])
            print(isbnInfo)
            base_reader = csv.reader(base, delimiter = ",")
            writer = csv.writer(result)
            line_count = 0
            for line in base_reader:
                if line_count == 0:
                    writer.writerow(line)
                    line_count += 1
                else:
                    if line[0] in isbnInfo:
                        writer.writerow(line)


