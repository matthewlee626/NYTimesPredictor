# TODO: implement the hasher: ie sum of squared genre frequencies divided by categories normalized
import csv
import json
import numpy as np

yesorno = "yes"

YEARS = ["2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","1997","1996","1995","1994","1993","1992","1991","1990","1989","1988","1987","1986","1985","1984","1983","1982","1981","1980","1979","1978","1977","1976","1975","1974","1973","1972","1971","1970","1969","1968","1967","1966","1965","1964","1963","1962","1961","1960","1959","1958","1957","1956","1955","1954","1953","1952","1951","1950","1949","1948","1947","1946","1945","1944","1943","1942","1941","1940","1939","1938","1937","1936","1935","1934","1933","1932","1931","1930","1929","1928","1927","1926","1925","1924","1923","1922","1921","1920","1919","1918","1917","1916","1915","1914","1913","1912","1911","1910","1909","1908","1907","1906","1905","1904","1903","1902","1901","1900"]

subjectHash = open("yesSubjectHash.csv", mode='r', encoding='utf-8')
placeHash = open("yesPlaceHash.csv", mode='r', encoding='utf-8')

#subjectwriter = csv.writer(subjectHash)
#placewriter = csv.writer(placeHash)

subjectreader = csv.reader(subjectHash, delimiter=',')
placereader = csv.reader(placeHash, delimiter=',')

with open(yesorno + ".json", mode='r') as inputs:
    with open(yesorno + ".csv", mode='w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output)

        isbnInfo = [line for line in inputs]

        places = {}
        subjects = {}
        peoples = {}
        '''
        #subjecthash = {}

        for entry in isbnInfo:
            entryloaded = json.loads(entry)
            key = list(entryloaded.keys())[0]

            # place hash
            if "subject_places" in entryloaded[key]:
                for place in entryloaded[key]["subject_places"]:
                    if place["name"] in places.keys():
                        places[place["name"]] += 1
                    else:
                        places[place["name"]] = 1

            # subject
            if "subjects" in entryloaded[key]:
                for subject in entryloaded[key]["subjects"]:
                    if subject["name"] in subjects.keys():
                        subjects[subject["name"]] += 1
                    else:
                        subjects[subject["name"]] = 1

           
            # people
            if "subject_people" in entryloaded[key]:
                for people in entryloaded[key]["subject_people"]:
                    if people["name"] in peoples.keys():
                        peoples[people["name"]] += 1
                    else:
                        peoples[people["name"]] = 1
            '''
        '''
        # removing subject fiction and protected DAISY while storing the hash
        counter = 0
        s = [(k, subjects[k]) for k in sorted(subjects, key=subjects.get, reverse=True)]
        for k, v in s:
            subjectwriter.writerow([k, v])
            if counter > 1:
                subjecthash[k] = v
            counter += 1
        s = [(k, places[k]) for k in sorted(places, key=places.get, reverse=True)]
        for k, v in s:
            placewriter.writerow([k, v])
        # writing the csv
        '''
        subject_count = 0

        for row in subjectreader:
            if subject_count > 1:
                subjects[row[0]] = int(row[1])
            subject_count += 1

        print(subjects)

        for row in placereader:
            places[row[0]] = int(row[1])

        print(places)

        writer.writerow(["ISBN", "Author", "Publisher", "Dewey", "LC", "Title", "Number of Pages", "Publish Place", "Subject Place", "Subject", "Publish Date"])

        for entry in isbnInfo:
            params = []

            entryloaded = json.loads(entry)
            key = list(entryloaded.keys())[0]
            params.append(key[5:])

            # author
            if "authors" in entryloaded[key]:
                params.append(entryloaded[key]['authors'][0]['name'])
            else:
                params.append(np.nan)

            # publisher
            if "publishers" in entryloaded[key]:
                params.append(entryloaded[key]['publishers'][0]['name'])
            else:
                params.append(np.nan)

            # dewey decimal
            if 'classifications' in entryloaded[key]:
                if "dewey_decimal_class" in entryloaded[key]['classifications']:
                    params.append(entryloaded[key]['classifications']['dewey_decimal_class'][0])
                else:
                    params.append(np.nan)
            else:
                params.append(np.nan)

            # library of congress classification
            if 'classifications' in entryloaded[key]:
                if "lc_classifications" in entryloaded[key]['classifications']:
                    params.append(entryloaded[key]['classifications']['lc_classifications'][0])
                else:
                    params.append(np.nan)
            else:
                params.append(np.nan)

            # title
            if "title" in entryloaded[key]:
                params.append(entryloaded[key]['title'])
            else:
                params.append(np.nan)

            # number of pages
            if "number_of_pages" in entryloaded[key]:
                params.append(entryloaded[key]["number_of_pages"])
            else:
                params.append(np.nan)

            # publish place
            if 'publish_places' in entryloaded[key]:
                params.append(entryloaded[key]['publish_places'][0]['name'])
            else:
                params.append(np.nan)

            # subject place param value
            placevalue = 0
            if "subject_places" in entryloaded[key]:
                for place in entryloaded[key]["subject_places"]:
                    if place["name"] in places.keys():
                        placevalue += places[place["name"]]
                if len(entryloaded[key]["subject_places"]) != 0:
                    params.append(placevalue/len(entryloaded[key]["subject_places"]))
                else:
                    params.append(placevalue)
            else:
                params.append(placevalue)

            # subject hash value
            subjectvalue = 0
            if "subjects" in entryloaded[key]:
                for subject in entryloaded[key]["subjects"]:
                    if subject["name"] in subjects.keys():
                        subjectvalue += subjects[subject["name"]]
                if len(entryloaded[key]["subjects"]) != 0:
                    params.append(subjectvalue/len(entryloaded[key]["subjects"]))
                else:
                    params.append(subjectvalue)
            else:
                params.append(subjectvalue)

            # publish place
            if 'publish_date' in entryloaded[key]:
                raw_date = entryloaded[key]['publish_date']
                for year in YEARS:
                    if raw_date.find(year) != -1:
                        params.append(year)
                        break
            else:
                params.append(np.nan)

            writer.writerow(params)

#subjectHash.close()
#placeHash.close()