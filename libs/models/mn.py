import pandas as pd
import numpy as np
# from sklearn.linear_model import RidgeCV
# from sklearn.metrics import mean_absolute_error as mae
# from scipy import stats
# import matplotlib.pyplot as plt
import os.path
# from sklearn.metrics import r2_score
# from sklearn.metrics.scorer import make_scorer
import math
# import statsmodels.api as sm
# import time
from keras import Sequential
from keras.layers import Dense, LSTM

# read in data
fiction = pd.read_csv("fiction.csv", delimiter=",")
# nonfiction = pd.read_csv("/Users/johanl/Downloads/nonfiction.csv", delimiter=",")
isbnToInfo = pd.read_csv("isbnToInfo.csv", delimiter=",")
genreData = pd.read_csv("sortedGenresFiction.csv", delimiter=",")
genreData.fillna(0, inplace=True)  # replace na with 0

def getMatrix(given_csv, k):
    sorted = {}

    # format into dictionary
    for i in range(given_csv.shape[0]):  # per day
        for j in range(1, 21):  # per entry
            if given_csv.iloc[i, j] in sorted:  # if key exist
                sorted[given_csv.iloc[i, j]].append([given_csv.iloc[i, 0], j])
            else:  # key doesn't exist
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

    print(clean)

    # add first 3
    nX = []
    nY = []
    nList = []
    maeList = []
    goodISBNs = []
    badEntriesIndex = []

    for i in clean.keys():
        nX.append(clean[i][0:3])

    print('nx length = ', len(nX))

    # graphing a specific book
    wannaCheckIsbn = '0525952926'
    wannaCheckIsbnIndex = 0
    wannaCheckIsbnPredictions = []
    wannaCheckIsbnActual = clean[wannaCheckIsbn][0:k]

    # model
    for n in range(3, k):

        params = []
        nList.append(n)
        nY.clear()

        for j in clean.keys():
            nY.append(clean[j][n])
            goodISBNs.append(j)

        for i in range(len(nX)):  # per book

            # ranking
            # slope, intercept, r_value, p_value, std_err = stats.linregress(list(range(len(nX[i]))), nX[i])
            model = np.polyfit(list(range(len(nX[i]))), nX[i], 2)
            last = nX[i][len(nX[i]) - 1]
            slope = model[0]
            slope1 = model[1]

            # genre
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

            for j in range(curWeek - 3, curWeek):
                prevGenrePercent.append(genreData[[curGenre]].iloc[j][0])

            # gSlope, gIntercept, gR_value, gP_value, gStd_err = stats.linregress(list(range(len(prevGenrePercent))), prevGenrePercent)
            model = np.polyfit(list(range(len(prevGenrePercent))), prevGenrePercent, 2)
            gSlope0 = model[0]
            gSlope1 = model[1]

            # searches
            curISBNnoZero = curISBN[1:]
            if os.path.exists(
                    "C:\\Users\\matth\\Desktop\\NYTimesPredictor\\datadump\\" + curISBN + ".csv"):  # for now, until we get all the data
                curSearchesDirty = pd.read_csv(
                    "C:\\Users\\matth\\Desktop\\NYTimesPredictor\\datadump\\" + curISBN + ".csv",
                    delimiter=",")  # cuz not clean
            elif os.path.exists("C:\\Users\\matth\\Desktop\\NYTimesPredictor\\datadump\\" + curISBNnoZero + ".csv"):
                curSearchesDirty = pd.read_csv(
                    "C:\\Users\\matth\\Desktop\\NYTimesPredictor\\datadump\\" + curISBNnoZero + ".csv", delimiter=",")
            else:
                goodISBNs.remove(curISBN)
                # if n > 3:
                #     print('suprise!')
                badEntriesIndex.append(i)
                continue
            curSearchesBusty = curSearchesDirty[['GT_SearchIndex']].values.tolist()  # busty cuz not flat
            curSearches = [item for sublist in curSearchesBusty for item in sublist]  # flatten
            if len(curSearches) == 0:  # if file empty
                badEntriesIndex.append(i)
                continue

            count = 0
            for j in curSearches:
                if j == 0:  # if searches that day is 0
                    count += 1

            if count / len(curSearches) > 0.25:  # if more than 25% of the searches is 0, change to weekly
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
                        if totalIterations < 7 * (k + 4):  # cuz start data starts from 1 month before
                            curSearchesWeekly.append(accumalativeSearches)
                            accumalativeSearches = 0
                            count = 0

            elif count / len(curSearches) <= 0.25:
                curSearchesWeekly = []
                totalIterations = 0

                for j in curSearches:
                    # for j in curSearches[4:]:
                    if totalIterations < 7 * (k + 4):
                        totalIterations += 1
                        curSearchesWeekly.append(j)  # well its rly daily searches but too lazy to make another var

            if len(curSearchesWeekly) < k:
                badEntriesIndex.append(i)


    print(len(nX))

    #####################################
    #####################################
    #####################################
    #####################################
    #####################################
    #####################################

    matrix = []
    bullshitassbullshit = []
    sorted = {}

    # format into dictionary
    for i in range(given_csv.shape[0]):  # per day
        for j in range(1, 21):  # per entry
            if given_csv.iloc[i, j] in sorted:  # if key exist
                sorted[given_csv.iloc[i, j]].append([given_csv.iloc[i, 0], j])
            else:  # key doesn't exist
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
    nY = []
    nList = []
    maeList = []
    # goodISBNs = []
    badEntriesIndex = []

    for i in clean.keys():
        nX.append(clean[i][0:k])


    xlength = len(clean.keys())
    ylength = k
    zlength = 3

    for a in range(xlength):  # num of books

        if a in badEntriesIndex:
            continue

        tempArray2 = []
        for b in range(ylength):  # num of weeks
            tempArray = []

            for c in range(3):
                tempArray.append(0)
            tempArray2.append(tempArray)
        matrix.append(tempArray2)

    print(np.shape(matrix))

    for a in range(xlength):  # num of books

        #####################################
        # genre
        curISBN = isbns[a]

        listI = isbnToInfo[['isbn']].values.tolist()
        flattenedI = [item for sublist in listI for item in sublist]
        curi = flattenedI.index(curISBN)
        curGenre = isbnToInfo[['Category']].iloc[curi][0]

        if "/" in curGenre:  # take first genre if there are 2
            curGenre = curGenre.split("/")[0]
        listG = fiction[['date']].values.tolist()
        flattened = [item for sublist in listG for item in sublist]
        curWeek = flattened.index(weeks[curISBN][0])

        # searches
        curISBNnoZero = curISBN[1:]
        if os.path.isfile(
                "/Users/johanl/Documents/GitHub/NYTimesPredictor/datadump/" + curISBN + ".csv"):  # for now, until we get all the data
            curSearchesDirty = pd.read_csv(
                "/Users/johanl/Documents/GitHub/NYTimesPredictor/datadump/" + curISBN + ".csv",
                delimiter=",")  # cuz not clean
        elif os.path.isfile("/Users/johanl/Documents/GitHub/NYTimesPredictor/datadump/" + curISBNnoZero + ".csv"):
            curSearchesDirty = pd.read_csv(
                "/Users/johanl/Documents/GitHub/NYTimesPredictor/datadump/" + curISBNnoZero + ".csv", delimiter=",")
        else:
            # goodISBNs.remove(curISBN)
            badEntriesIndex.append(a)
            continue
        curSearchesBusty = curSearchesDirty[['GT_SearchIndex']].values.tolist()  # busty cuz not flat
        curSearches = [item for sublist in curSearchesBusty for item in sublist]  # flatten
        if len(curSearches) == 0:  # if file empty
            badEntriesIndex.append(a)
            continue

        count = 0
        for j in curSearches:
            if j == 0:  # if searches that day is 0
                count += 1

        # if count / len(curSearches) > 0.25 and len(curSearches)/7 >= k:  # if more than 25% of the searches is 0, change to weekly
        # if True:
        #     curSearchesWeekly = []
        #     count = 0
        #     accumalativeSearches = 0
        #     totalIterations = 0
        #     howMany = math.floor(len(curSearches) / k)
        #     for j in curSearches[4:(7*k + 4)]:
        #         # for j in curSearches[4:]:
        #
        #         totalIterations += 1
        #         count += 1
        #         accumalativeSearches += j
        #         if count == howMany:  # every 7 days (1 week), we record the sales that week
        #             # if totalIterations < 7 * (k + 4):  # cuz start data starts from 1 month before
        #             if True:
        #                 curSearchesWeekly.append(accumalativeSearches)
        #                 accumalativeSearches = 0
        #                 count = 0
        curSearchesWeekly = []
        for j in range(k):
            howMany = math.floor(len(curSearches)/k)
            curSearchesWeekly.append(curSearches[(j*howMany): (j*howMany+1)])

        # elif count / len(curSearches) <= 0.25:
        #     curSearchesWeekly = []
        #     totalIterations = 0
        #
        #     for j in curSearches[4:]:
        #         # for j in curSearches[4:]:
        #         if totalIterations < 7 * (k + 4):
        #             totalIterations += 1
        #             curSearchesWeekly.append(j)  # well its rly daily searches but too lazy to make another var


        #####################################

        for b in range(ylength):  # num of weeks
            # past, genre, google

            # print(matrix)
            if b < k:
                matrix[a][b][0] = nX[a][b]
                matrix[a][b][1] = genreData[[curGenre]].iloc[curWeek][0]
                try:
                    # print(b, curSearchesWeekly)
                    matrix[a][b][2] = curSearchesWeekly[b]
                except:
                    # del matrix[a][b]
                    # print(b, len(curSearchesWeekly))
                    bullshitassbullshit.append([a, b])
            else:
                matriy[a][0] = nX[a][b]
                matriy[a][1] = genreData[[curGenre]].iloc[curWeek][0]
                matriy[a][2] = curSearchesWeekly[b]

    print(bullshitassbullshit)
    # for i in reversed(bullshitassbullshit):
    #     print(i[0])
    #     print(i[1])

        # del matrix[i[0]][i[1]]

    # print(matrix)
    # print(np.shape(matrix))

    matrix = np.asarray(matrix)
    print(np.shape(matrix))



getMatrix(fiction, 7)

# import keras
# from keras import backend as K
#
#
# class MinimalRNNCell(keras.layers.Layer):
#
#     def __init__(self, units, **kwargs):
#         self.units = units
#         self.state_size = units
#         super(MinimalRNNCell, self).__init__(**kwargs)
#
#     def build(self, input_shape):
#         self.kernel = self.add_weight(shape=(input_shape[-1], self.units),
#                                       initializer='uniform',
#                                       name='kernel')
#         self.recurrent_kernel = self.add_weight(
#             shape=(self.units, self.units),
#             initializer='uniform',
#             name='recurrent_kernel')
#         self.built = True
#
#     def call(self, inputs, states):
#         prev_output = states[0]
#         h = K.dot(inputs, self.kernel)
#         output = h + K.dot(prev_output, self.recurrent_kernel)
#         return output, [output]
#
#
# # # Let's use this cell in a RNN layer:
# # cell = MinimalRNNCell(32)
# # x = keras.Input((None, 5))
# # layer = keras.RNN(cell)
# # y = layer(x)
#
# # Here's how to use the cell to build a stacked RNN:
#
# cells = [MinimalRNNCell(32), MinimalRNNCell(64)]
# x = keras.Input((None, 5))
# layer = keras.RNN(cells)
# y = layer(x)
#
# kerasLayer = keras.layers.SimpleRNN(units, activation='tanh',
#                        use_bias=True, kernel_initializer='glorot_uniform',
#                        recurrent_initializer='orthogonal',
#                        bias_initializer='zeros', kernel_regularizer=None,
#                        recurrent_regularizer=None, bias_regularizer=None,
#                        activity_regularizer=None, kernel_constraint=None,
#                        recurrent_constraint=None, bias_constraint=None,
#                        dropout=0.0, recurrent_dropout=0.0,
#                        return_sequences=False, return_state=False,
#                        go_backwards=False, stateful=False, unroll=False)
# model = MinimalRNNCell(kerasLayer)
# # model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# # model.fit(X, y, epochs=150, batch_size=10)
# # _, accuracy = model.evaluate(X, y)
#
#
# #for t sequences (num of samples), 2nd is length of samples (10 weeks), 3rd is # of features
