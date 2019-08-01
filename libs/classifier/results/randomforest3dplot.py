from sklearn import datasets
import pandas as pd
from tqdm import tqdm

books_ds = pd.read_csv('books_dataset_v5_titlefixed_titleinfo.csv')

from sklearn.model_selection import train_test_split
X = books_ds[['Number of Pages', 'Subject Place', 'Subject', 'publisher_id', 'publishplace_id', 'dewey_id', 'publisher_freq', 'publish_place_freq', 'dewey_freq', 'author_id', 'author_frequency', 'title_avg_word_len', 'title_num_words']]
#removed publish date
y = books_ds['on_NYT']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=25)

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators = 100)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

from sklearn import metrics
print('Accuracy:', metrics.accuracy_score(y_test, y_pred))

feature_imp = pd.Series(clf.feature_importances_, index=['Number of Pages', 'Subject Place', 'Subject', 'publisher_id', 'publishplace_id', 'dewey_id', 'publisher_freq', 'publish_place_freq', 'dewey_freq', 'author_id', 'author_frequency', 'title_avg_word_len', 'title_num_words' ]).sort_values(ascending=False)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

books_ds_fig = pd.read_csv('books_dataset_v5_titlefixed_titleinfo.csv', index_col='on_NYT')
books_ds_fig.head()

subject_score = []
author_frequency = []
publisher_frequency = []
markers = []

for i in range(books_ds_fig.shape[0]):
    subject_score.append(books_ds_fig['Subject'])
    author_frequency.append(books_ds_fig['author_frequency'])
    publisher_frequency.append(books_ds_fig['publisher_freq'])
    if books_ds_fig.index[i] == 0:
        markers.append('o')
    elif books_ds_fig.index[i] == 1:    
        markers.append('^')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('Subjecet')
ax.set_ylabel('Author Frequecy')
ax.set_zlabel('Publisher Frequency')

for i in tqdm(range(books_ds.shape[0])):
    ax.scatter(subject_score[i], author_frequency[i], publisher_frequency[i], marker=markers[i])

print('Plotted')
plt.show()
