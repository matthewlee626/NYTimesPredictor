import pandas as pd
import numpy as np
import sklearn as skl
from sklearn.linear_model import RidgeCV
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

    print(maeList)
    #plt.plot(nList, maeList)
    #plt.show()
    #print(keys)
    #for key in range(len(keys)):
        #print(clean[keys[key]][0:k])
        #print(nX[keyindex[key]][0:k])

predict(fiction, 10)



# xSlope = []
# realY = []
#
# # we pass in features of: slope of rankings + last rankings (pray) both weights are 1, then other features
# # or we pass predicted
#
# # list.append model.coef
# # model.coef_ = np.array(ARRAY)
#
# # slope of last ranking
# for i in range(len(nX)):
#     print(list(range(n)))
#     print(nX[i])
#     # print(np.array([list(range(n)), nX[i]]))
#     # formattedX = pd.DataFrame(data=np.array([list(range(n)), nX[i]]), index=(2, 3), columns=['index', 'past'])
#
#     # formattedX = np.asarray(nX[i])
#     # formattedX = pd.DataFrame(data=np.asarray(nX[i]), columns=['past'])
#
#     temp = []
#     for j in range(n):
#
#
#     formattedX = pd.DataFrame(columns=("index", 'rank_slope'))
#     print(formattedX)
#     formattedX.iloc[0] = list(range(n))
#     formattedX.iloc[len(formattedX)] = nX[i]
#     print(formattedX)
#
#     # testY = pd.DataFrame([np.asarray([n]), np.asarray(nY[i])], columns=['past'])
#
#     classifier = LinearRegression(fit_intercept=False)
#     # print(testY)
#     classifier.fit(formattedX, nY[i])  # .fit(X, y)
#
#     xSlope.append(classifier.coef_)
#     future = classifier.predict(formattedX).tolist()
#
#
#
# # total model
#
# #add previous and slope
# formattedX = pd.DataFrame(np.asarray(xSlope), columns=['prev_slope'])
# prev = np.asarray(nX[:, len(nX[0])])
# formattedX.insert(1, 'prev', prev)
#
# # add genre
#
# classifier = RidgeCV()
# classifier.fit(formattedX, nY)
# future = classifier.predict(formattedX).tolist()
#
# maeList.append((mae(nY, future)))
#
# # add pred value to X
# for j in range(len(future)):
#     future[j] = round(future[i])
#
# for k in range(len(nX)):
#     nX[k].append(future[k])

#
# sortedFiction = {}
#
# for i in range(fiction.shape[0]): #per day
#     for j in range(1, 21): #per entry
#         if fiction.iloc[i, j] in sortedFiction: #if key exist
#             sortedFiction[fiction.iloc[i, j]].append([fiction.iloc[i, 0], j])
#         else: #key doesn't exist
#             sortedFiction[fiction.iloc[i, j]] = [[fiction.iloc[i, 0], j]]
#
# print(sortedFiction)
#
# #remove ones that have less than k entries since hard to predict
# k = 10
#
# cleanFiction = {}
# for i in sortedFiction.keys():
#     if len(sortedFiction[i]) >= k:
#         cleanFiction[i] = []
#         for j in sortedFiction[i]:
#             cleanFiction[i].append(j[1])
#
# #print(cleanFiction)
# print(len(cleanFiction.keys()))
#
# print(cleanFiction)
#
# #
# # #save file
# # csv_file = "sortedRankingsFiction.csv"
# #
# # with open(csv_file, 'w') as output:
# #
# #     for key in cleanFiction.keys():
# #         output.write("%s,%s\n"%(key,cleanFiction[key]))
#
#
# #ridge predict n+1th one
#
# #input data wiht n values
#
# nX = []
# nY = []
# nList = []
# maeList = []
#
# for i in cleanFiction.keys():
#     nX.append(cleanFiction[i][0:3])
#
# for n in range(3, k):
#
#     # nFictionY.append(cleanFiction[i][n])
#
#
# # training
# classifier = RidgeCV()
# classifier.fit(nFictionX, nFictionY)  # .fit(X, y)
#
# print(classifier.coef_)
#
#
#
# # # save file
# # csv_file = "cleanRankingsFiction.csv"
# #
# # with open(csv_file, 'w') as output:
# #
# #     for key in cleanFiction.keys():
# #         output.write("%s,%s\n"%(key,cleanFiction[key]))

