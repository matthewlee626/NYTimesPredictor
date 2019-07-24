import pandas as pd
import sklearn as skl
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error as mae
import matplotlib.pyplot as plt
from scipy import stats
import csv
import numpy as np

fiction = pd.read_csv("fiction.csv", delimiter=",")
nonfiction = pd.read_csv("nonfiction.csv", delimiter=",")
isbnToInfo = pd.read_csv("isbnToInfo.csv", delimiter=",")
genreData = pd.read_csv("sortedGenresFiction.csv", delimiter=",")
genreData.fillna(0, inplace=True)  # replace na with 0

def predict(given_csv, k, colorstart):
    titles = []
    sorted = {}

    for i in range(given_csv.shape[0]): #per day
        for j in range(1, 21): #per entry
            if given_csv.iloc[i, j] in sorted: #if key exist
                sorted[given_csv.iloc[i, j]].append([given_csv.iloc[i, 0], j])
            else: #key doesn't exist
                sorted[given_csv.iloc[i, j]] = [[given_csv.iloc[i, 0], j]]

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

    nX = []
    nY = []
    nList = [] # our time, per say
    maeList = []

    # purely for graphing
    key_counter = 0
    keys = []
    keyindex = [73]

    n = 3

    # remove isbn
    isbns = list(clean.keys())

    for i in clean.keys():
        for neededindex in keyindex:
            if key_counter == neededindex:
                keys.append(i)
        key_counter += 1

        nX.append(clean[i][0:n])

    # training
    classifier = LinearRegression()

    # count = 0
    for n in range(3, k):
        parameters = []
        degree = 2

        nList.append(n)
        nY.clear()
        for j in clean.keys():
            nY.append(clean[j][n])

        for item in range(len(nX)):

            # previous rank
            coefs = np.polyfit(list(range(len(nX[item]))), nX[item], 2)

            last = nX[item][len(nX[item]) - 1]

            coefsFinal = list(coefs)[:len(coefs)-1]
            coefsFinal.append(last)

            # genre
            curISBN = isbns[item]

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

            for j in range(curWeek - 3, curWeek):
                prevGenrePercent.append(genreData[[curGenre]].iloc[j][0])
            # gSlope, gIntercept, gR_value, gP_value, gStd_err = stats.linregress(list(range(len(prevGenrePercent))), prevGenrePercent)
            gcoefs = np.polyfit(list(range(len(prevGenrePercent))), prevGenrePercent, 2)
            gcoefsFinal = list(gcoefs)[:len(gcoefs) - 1]
            gcoefsFinal.append(last)


            parameters.append(coefsFinal + gcoefsFinal)

        for params in parameters:
            for e in range(2, degree+1):
                for length in range(len(params)):
                    params.append(pow(params[length], e))

        print(parameters, nY)
        classifier.fit(parameters, nY)  # .fit(X, y)
        future = classifier.predict(parameters).tolist()
        for i in range(len(future)):
            future[i] = round(future[i])

        for p in range(len(nX)):
            # print(len(future))
            # print(len(nX))
            nX[p].append(future[p])
        maeList.append((mae(nY, future)))

    '''
    print(nList)
    print(maeList)
    plt.plot(nList, maeList)
    plt.show()
    '''
    missingValues = [0, 1, 2]
    nList = missingValues + nList

    with open('titleISBNdate.csv', mode='r', encoding='utf-8') as info:
        reader = csv.reader(info, delimiter=',')
        for line in reader:
            for isbn in keys:
                if line[0] == isbn:
                    titles.append(line[1])

    colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#ffff99']
    for key in range(len(keys)):
        color = colors[key+colorstart]
        plt.plot(nList, clean[keys[key]][0:k], label='Actual: ' + titles[key], color=color)
        plt.plot(nList, nX[keyindex[key]][0:k], label='Predicted: ' + titles[key], linestyle=':', color=color)
        #print(keys)
        #print(clean[keys[key]][0:k])
        #print(nX[keyindex[key]][0:k])
    plt.title("First Model: Building NYTimes Best Seller Path by predicting the n+1th ranking from the first n rankings")
    #print(maeList)
    #plt.plot(nList, maeList)

    #print(count)

    plt.legend()
    #plt.show()


predict(fiction, 10, 0)
#predict(nonfiction, 10, 4)
plt.ylim(0, 20)
plt.gca().invert_yaxis()
plt.show()
