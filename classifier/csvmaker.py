# TODO: implement the hasher: ie sum of squared genre frequencies divided by categories normalized
import csv
import json
import numpy as np

yesorno = "no"

subjectHash = open(yesorno + "SubjectHash.csv", mode='w', encoding='utf-8', newline='')
placeHash = open(yesorno + "PlaceHash.csv", mode='w', encoding='utf-8', newline='')

subjectwriter = csv.writer(subjectHash)
placewriter = csv.writer(placeHash)

with open(yesorno + ".json", mode='r') as inputs:
    with open(yesorno + ".csv", mode='w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output)

        isbnInfo = [line for line in inputs]
        places = {}
        subjects = {}
        peoples = {}

        subjecthash = {}

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

            '''
            # people
            if "subject_people" in entryloaded[key]:
                for people in entryloaded[key]["subject_people"]:
                    if people["name"] in peoples.keys():
                        peoples[people["name"]] += 1
                    else:
                        peoples[people["name"]] = 1
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

        writer.writerow(["Publisher", "Dewey", "LC", "Title", "Number of Pages", "Publish Place", "Subject Place", "Subject"])

        for entry in isbnInfo:
            params = []

            entryloaded = json.loads(entry)
            key = list(entryloaded.keys())[0]

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
                if "lc_classification" in entryloaded[key]['classifications']:
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

            writer.writerow(params)

subjectHash.close()
placeHash.close()