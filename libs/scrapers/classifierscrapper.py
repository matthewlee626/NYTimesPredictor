import csv
import json
import requests

with open('isbns/unique_isbn_v2.csv', mode='r') as fiction_input:
    with open('unique_isbn_v2.json', mode='w') as output:
        reader = csv.reader(fiction_input, delimiter=' ')
        line_count = 0
        for row in reader:
            row_array = row[0].split('\t')
            if line_count == 0:
                line_count += 1
            else:
                print(row_array[1])
                r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:'+row_array[1]+'&format=json&jscmd=data')
                json.dump(r.json(), output)
                output.write("\n")
                line_count += 1