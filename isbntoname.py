import csv
import requests
import json


def main():
    isbn_list = []
    with open('fiction.csv') as fiction_input:
        with open('nonfiction.csv') as nonfiction_input:
            with open('isbnData.json', mode='w') as output:
                fiction_reader = csv.reader(fiction_input, delimiter=',')
                nonfiction_reader = csv.reader(nonfiction_input, delimiter=',')
                line_count = 0
                for row in fiction_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        for i in range(1, 21):
                            if row[i] not in isbn_list:
                                isbn_list.append(row[i])
                                r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:'+row[i]+'&format=json&jscmd=data')
                                json.dump(r.json(), output)
                                output.write("\n")
                        line_count += 1
                line_count = 0
                for row in nonfiction_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        for i in range(1, 21):
                            if row[i] not in isbn_list:
                                isbn_list.append(row[i])
                                r = requests.get(
                                    'https://openlibrary.org/api/books?bibkeys=ISBN:' + row[i] + '&format=json&jscmd=data')
                                json.dump(r.json(), output)
                                output.write("\n")
                        line_count += 1


if __name__ == '__main__':
    main()
