import csv
import requests
import json

#ISBN scrapper function
def main():
    isbn_list = []
    with open('isbns/unique_notNYT_isbn.csv', mode='r') as fiction_input:
        with open('unique_notNYT_isbn_json.json', mode='w') as output:
            reader = csv.reader(fiction_input, delimiter=' ')
            line_count = 0
            for row in reader:
                row_array = row[0].split('\t')
                if line_count == 0:
                    line_count += 1
                else:
                    r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:'+ row_array[1] +'&format=json&jscmd=data')
                    json.dump(r.json(), output)
                    output.write("\n")
                    line_count += 1


if __name__ == '__main__':
    main()
