import pandas as pd
import numpy as np
import sklearn as skl
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error as mae
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import csv


fiction = pd.read_csv("fiction.csv", delimiter= ",")
nonfiction = pd.read_csv("nonfiction.csv", delimiter= ",")
isbnToInfo = pd.read_csv("isbnToInfo.csv", delimiter= ",")
genreData = pd.read_csv("sortedGenresFiction.csv", delimiter= ",")
genreData.fillna(0, inplace=True)

def predict(given_csv, k):
    sorted = {}

    for i in range(given_csv.shape[0]): #per day
        for j in range(1, 21): #per entry
            if given_csv.iloc[i, j] in sorted: #if key exist
                sorted[given_csv.iloc[i, j]].append([given_csv.iloc[i, 0], j])
            else: #key doesn't exist
                sorted[given_csv.iloc[i, j]] = [[given_csv.iloc[i, 0], j]]

    #print(sortedFiction)

    #remove ones that have less than k entries since hard to predict

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


    #ridge predict n+1th one

    #input data wiht n values

    nX = []
    nY = []
    nList = []
    maeList = []

    key_counter = 0
    keys = []
    keyindex = [73]

    n = 3

    # remove isbn
    for i in clean.keys():
        for neededindex in keyindex:
            if key_counter == neededindex:
                keys.append(i)
        key_counter += 1

    for i in clean.keys():
        nX.append(clean[i][0:3])

    for n in range(3, k):

        params = []
        nList.append(n)
        nY.clear()
        for j in clean.keys():
            nY.append(clean[j][n])

        for i in range(len(nX)): # per book
            #print(nX)
            #ranking
            #slope, intercept, r_value, p_value, std_err = stats.linregress(list(range(len(nX[i]))), nX[i])
            coefs = np.polyfit(list(range(len(nX[i]))), nX[i], 2)
            last = nX[i][len(nX[i]) - 1]

            #genre
            curISBN = isbns[i]


            listI = isbnToInfo[['isbn']].values.tolist()
            flattenedI = [item for sublist in listI for item in sublist]
            curi = flattenedI.index(curISBN)
            curGenre = isbnToInfo[['Category']].iloc[curi][0]

            if "/" in curGenre:
                curGenre = curGenre.split("/")[0]
            prevGenrePercent = []
            listG = fiction[['date']].values.tolist()
            flattened = [item for sublist in listG for item in sublist]
            curWeek = flattened.index(weeks[curISBN][0])

            for j in range(curWeek-3, curWeek):
                prevGenrePercent.append(genreData[[curGenre]].iloc[j][0])
            gSlope, gIntercept, gR_value, gP_value, gStd_err = stats.linregress(list(range(len(prevGenrePercent))), prevGenrePercent)

            params.append([coefs[0], coefs[1], last, gSlope])

        #train
        degree = 2
        #print(parameters)
        for param in params:
            #print(param)
            for e in range(2, degree+1):
                #print(e)
                for length in range(len(param)):
                    #print(length)
                    #print(pow(params[length], e))
                    param.append(pow(param[length], e))
            #print(params)
        #print(parameters)

        classifier = RidgeCV()
        classifier.fit(params, nY)
        future = classifier.predict(params).tolist()
        maeList.append((mae(nY, future)))

        for i in range(len(future)):
            future[i] = round(future[i])
        #print(future)
        #print(nX)
        for p in range(len(nX)):
            nX[p].append(future[p])

    print(maeList)
    #plt.plot(nList, maeList)
    #plt.show()
    #print(keys)
    #for key in range(len(keys)):
        #print(clean[keys[key]][0:k])
        #print(nX[keyindex[key]][0:k])


predict(fiction, 10)

