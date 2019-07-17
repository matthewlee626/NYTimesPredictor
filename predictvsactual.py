import pandas as pd
import sklearn as skl
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error as mae
import matplotlib.pyplot as plt
import math

fiction = pd.read_csv("fiction.csv", delimiter= ",")
nonfiction = pd.read_csv("nonfiction.csv", delimiter= ",")
isbnToInfo = pd.read_csv("isbnToInfo.csv", delimiter= ",")


def predict(given_csv):
    sorted = {}

    for i in range(given_csv.shape[0]): #per day
        for j in range(1, 21): #per entry
            if given_csv.iloc[i, j] in sorted: #if key exist
                sorted[given_csv.iloc[i, j]].append([given_csv.iloc[i, 0], j])
            else: #key doesn't exist
                sorted[given_csv.iloc[i, j]] = [[given_csv.iloc[i, 0], j]]

    #print(sortedFiction)

    #remove ones that have less than k entries since hard to predict
    k = 10

    clean = {}
    for i in sorted.keys():
        if len(sorted[i]) >= k:
            clean[i] = []
            for j in sorted[i]:
                clean[i].append(j[1])

    #print(cleanFiction)
    print(len(clean.keys()))

    #ridge predict n+1th one

    #input data wiht n values

    nX = []
    nY = []
    nList = []
    maeList = []

    for i in clean.keys():
        nX.append(clean[i][0:3])

    for n in range(3, k):
        nList.append(n)
        nY.clear()
        for j in clean.keys():
            nY.append(clean[j][n])

        #training
        classifier = RidgeCV()
        classifier.fit(nX, nY)  # .fit(X, y)
        future = classifier.predict(nX).tolist()
        for i in range(len(future)):
            future[i] = round(future[i])
        #print(nX)
        for k in range(len(nX)):
            nX[k].append(future[k])
        maeList.append((mae(nY, future)))

    print(maeList)
    plt.plot(nList, maeList)
    plt.show()


predict(nonfiction)
