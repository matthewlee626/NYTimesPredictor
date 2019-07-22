import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error as mae
from scipy import stats
import matplotlib.pyplot as plt
import os.path

# read in data
fiction = pd.read_csv("fiction.csv", delimiter=",")
nonfiction = pd.read_csv("nonfiction.csv", delimiter=",")
isbnToInfo = pd.read_csv("isbnToInfo.csv", delimiter=",")
genreData = pd.read_csv("sortedGenresFiction.csv", delimiter=",")
genreData.fillna(0, inplace=True)  # replace na with 0


def predict(given_csv, k):
    sorted = {}

    # format into dictionary
    for i in range(given_csv.shape[0]): # per day
        for j in range(1, 21): # per entry
            if given_csv.iloc[i, j] in sorted: # if key exist
                sorted[given_csv.iloc[i, j]].append([given_csv.iloc[i, 0], j])
            else: # key doesn't exist
                sorted[given_csv.iloc[i, j]] = [[given_csv.iloc[i, 0], j]]

    # remove ones that have less than k entries since hard to predict
    clean = {}
    weeks = {}
    for i in sorted.keys():
        if len(sorted[i]) >= k:
            clean[i] = []
            weeks[i] = []
            for j in sorted[i]:
                clean[i].append(j[1])
                weeks[i].append(j[0])

    isbns = list(clean.keys())

    # add first 3
    nX = []

    for i in clean.keys():
        nX.append(clean[i][0:3])

    print('nx length = ', len(nX))

    # model
    for n in range(3, k):

        badEntriesIndex = []
        for i in range(len(nX)):  # per book

            #genre
            curISBN = isbns[i]

            listI = isbnToInfo[['isbn']].values.tolist()
            flattenedI = [item for sublist in listI for item in sublist]
            curi = flattenedI.index(curISBN)
            curGenre = isbnToInfo[['Category']].iloc[curi][0]

            if "/" in curGenre:  # take first genre if there are 2
                curGenre = curGenre.split("/")[0]
            prevGenrePercent = []
            listG = fiction[['date']].values.tolist()
            flattened = [item for sublist in listG for item in sublist]
            curWeek = flattened.index(weeks[curISBN][0])


            #searches

            if os.path.isfile("datadump/" + curISBN + ".csv"): # for now, until we get all the data
                curSearchesDirty = pd.read_csv("datadump/" + curISBN + ".csv", delimiter=",")  # cuz not clean
            else:
                badEntriesIndex.append(i)
                # continue
            # curSearchesBusty = curSearchesDirty[['GT_SearchIndex']].values.tolist()  # busty cuz not flat
            # curSearches = [item for sublist in curSearchesBusty for item in sublist]  # flatten
            # if len(curSearches) == 0:  # if file empty
            #     print(curSearches)
            #     badEntriesIndex.append(i)
            #     continue
        print(len(badEntriesIndex))


predict(fiction, 6)
