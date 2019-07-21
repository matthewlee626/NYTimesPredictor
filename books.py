import pandas as pd
import numpy as np
import sklearn as skl
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error as mae
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import os.path
import numpy as np
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


    for i in clean.keys():
        nX.append(clean[i][0:3])

    for n in range(3, k):

        params = []
        nList.append(n)
        nY.clear()
        for j in clean.keys():
            nY.append(clean[j][n])

        # badEntries = set()
        badEntries = []
        for i in range(len(nX)):  # per book

            #ranking
            slope, intercept, r_value, p_value, std_err = stats.linregress(list(range(len(nX[i]))), nX[i])
            last = nX[i][len(nX[i]) - 1]


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

            for j in range(curWeek-3, curWeek):
                prevGenrePercent.append(genreData[[curGenre]].iloc[j][0])
            gSlope, gIntercept, gR_value, gP_value, gStd_err = stats.linregress(list(range(len(prevGenrePercent))), prevGenrePercent)


            #searches

            if os.path.isfile("datadump/" + curISBN + ".csv"): # for now, until we get all the data
                curSearchesDirty = pd.read_csv("datadump/" + curISBN + ".csv", delimiter=",")  # cuz not clean
            else:
                if curISBN not in badEntries:
                    # badEntries.add(curISBN)
                    badEntries.append(curISBN)
                continue
            curSearchesBusty = curSearchesDirty[['GT_SearchIndex']].values.tolist()  # busty cuz not flat
            curSearches = [item for sublist in curSearchesBusty for item in sublist]  # flatten
            if len(curSearches) == 0:  # if file empty
                if curISBN not in badEntries:
                    # badEntries.add(curISBN)
                    badEntries.append(curISBN)
                continue
            # // remember to leave in start form 1st week (start from 4)
            # data starts from month before
            count = 0
            for j in curSearches:
                if j == 0:  # if searches that day is 0
                    count += 1

            if count/len(curSearches) > 0.25:  # if more than 25% of the searches is 0, change to weekly
                curSearchesWeekly = []
                count = 0
                accumalativeSearches = 0
                totalIterations = 0
                for j in curSearches:
                # for j in curSearches[4:]:

                    totalIterations += 1
                    count += 1
                    accumalativeSearches += j
                    if count == 7:  # every 7 days (1 week), we record the sales that week
                        curSearchesWeekly.append(accumalativeSearches)
                        accumalativeSearches = 0
                        count = 0
                    if totalIterations == 7*(k+4):  # cuz start data starts from 1 month before
                        break

            elif count/len(curSearches) <= 0.25:
                curSearchesWeekly = []
                count = 0
                accumalativeSearches = 0
                totalIterations = 0
                for j in curSearches:
                # for j in curSearches[4:]:
                    totalIterations += 1
                    curSearchesWeekly.append(j)  # well its rly daily searches but too lazy to make another var
                    if totalIterations == 7*(k+4):
                        break

            coefsSearch = np.polyfit(list(range(len(curSearchesWeekly))), curSearchesWeekly, 3)

            if i == len(nX) - 1:
                f = np.poly1d(coefsSearch)
                xi = range(len(curSearchesWeekly))
                yi = f(xi)

                #plt.plot(xi, curSearchesWeekly, 'o', xi, yi)

            #print('data = ', curSearchesWeekly)
            #print('slope = ', sSlope)

            #append params
            params.append([slope, last, gSlope, coefsSearch[0], coefsSearch[1], coefsSearch[2]])

        #remove bad entries from nY
        # print('len', len(nY))
        # for j in reversed([value for value in list(clean.keys()) if value in list(badEntries)]):  #intersection of 2 lists, but reversed cuz deleting
            # print(isbns.index(j))
            # del nY[isbns.index(j)]
        #we're not looping in order... i wonder why

        for j in reversed(badEntries):
            # print(isbns.index(j))
            del nY[isbns.index(j)]

        degree = 2
        # print(parameters)
        for param in params:
            # print(param)
            for e in range(2, degree + 1):
                # print(e)
                for length in range(len(param)):
                    # print(length)
                    # print(pow(params[length], e))
                    param.append(pow(param[length], e))
            # print(params)
        # print(parameters)

        classifier = RidgeCV()
        classifier.fit(params, nY)
        print(params)
        future = classifier.predict(params).tolist()
        maeList.append((mae(nY, future)))

        for i in range(len(future)):
            future[i] = round(future[i])
        #print(future)
        #print(nX)
        for p in range(len(nX)):
            nX[p].append(future[p])
            
    print(classifier.coef_)

    print(maeList)
    plt.plot(nList, maeList)
    plt.show()


predict(fiction, 10)
