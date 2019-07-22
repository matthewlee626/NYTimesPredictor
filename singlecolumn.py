import csv
import requests


def main():
    isbn_list = []
    with open('fiction.csv', mode='r') as fiction_input:
        with open('fictionsingle.csv', mode='w', newline='') as output:
            reader = csv.reader(fiction_input, delimiter=',')
            writer = csv.writer(output)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    line_count += 1
                else:
                    for i in range(1, 21):
                        info = row[i]
                        isbn_list.append(info)
                    line_count += 1
            mylist = list(dict.fromkeys(isbn_list))
            print(mylist)
            for row2 in mylist:
                writer.writerow([row2])

if __name__ == '__main__':
    main()
