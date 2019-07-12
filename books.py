import pandas as pd
import sklearn as skl
from sklearn.linear_model import RidgeCV
from sklearn.metrics import r2_score

fiction = pd.read_csv("/Users/johanl/Downloads/fiction.csv", delimiter= ",")
nonfiction = pd.read_csv("/Users/johanl/Downloads/nonfiction.csv", delimiter= ",")
isbnToInfo = pd.read_csv("/Users/johanl/Downloads/isbnToInfo.csv", delimiter= ",")

sortedFiction = {}

for i in range(fiction.shape[0]): #per day
    for j in range(1, 21): #per entry
        if fiction.iloc[i, j] in sortedFiction: #if key exist
            sortedFiction[fiction.iloc[i, j]].append([fiction.iloc[i, 0], j])
        else: #key doesn't exist
            sortedFiction[fiction.iloc[i, j]] = [[fiction.iloc[i, 0], j]]

#print(sortedFiction)

#remove ones that have less than k entries since hard to predict
k = 4

cleanFiction = {}
for i in sortedFiction.keys():
    if len(sortedFiction[i]) >= k:
        cleanFiction[i] = []
        for j in sortedFiction[i]:
            cleanFiction[i].append(j[1])

#print(cleanFiction)
print(len(cleanFiction.keys()))

#ridge predict n+1th one

#input data wiht n values
n = k - 1

nFictionX = []
nFictionY = []
for i in cleanFiction.keys():
    nFictionX.append(cleanFiction[i][0:n])
    nFictionY.append(cleanFiction[i][n])

#training
classifier = RidgeCV()
classifier.fit(nFictionX, nFictionY)  # .fit(X, y)

#can make own scorer with make_scorer under metrics
classifier.score(nFictionX, nFictionY)
print(classifier.score(nFictionX, nFictionY))

#print(classifier)
