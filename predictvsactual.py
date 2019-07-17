import pandas as pd
import sklearn as skl
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error as mae
import matplotlib.pyplot as plt
import math
from scipy import stats
import csv

fiction = pd.read_csv("fiction.csv", delimiter= ",")
nonfiction = pd.read_csv("nonfiction.csv", delimiter= ",")
isbnToInfo = pd.read_csv("isbnToInfo.csv", delimiter= ",")

titles = []

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
    nList = [] # our time, per say
    maeList = []

    key_counter = 0
    keys = []
    keyindex = [12, 42, 69]

    n = 3

    for i in clean.keys():
        if key_counter == 69 or key_counter == 42 or key_counter == 12:
            keys.append(i)
        key_counter += 1
        nX.append(clean[i][0:n])
        nY.append(clean[i][n])

    # training
    classifier = RidgeCV()

    for n in range(3, k):
        #slopes = []
        #futures = []
        parameters = []

        nList.append(n)
        nY.clear()
        for j in clean.keys():
            nY.append(clean[j][n])

        for item in range(len(nX)):
            slope, intercept, r_value, p_value, std_err = stats.linregress(list(range(len(nX[item]))), nX[item])
            #slopes.append(slope)
            last = nX[item][len(nX[item]) - 1]
            #futures.append(prediction)
            parameters.append([slope, last])


        #training
        classifier.fit(parameters, nY)  # .fit(X, y)
        future = classifier.predict(parameters).tolist()
        for i in range(len(future)):
            future[i] = round(future[i])
        #print(nX)
        for p in range(len(nX)):
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
                    global titles
                    titles.append(line[1])

    for key in range(len(keys)):
        plt.plot(nList, clean[keys[key]][0:k], label='Actual')
        plt.plot(nList, nX[keyindex[key]][0:k], label='Predicted')
    plt.title(title for title in titles)
    plt.legend()
    plt.show()


predict(nonfiction, 10)
