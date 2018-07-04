from __future__ import division

import numpy as np
import sys
from pandas import read_csv
from scipy.stats import binom_test, expon 
from performance import confident_precision
from parse import get_train_data
from os import environ

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

id = environ['TARGET_CFD_ID']

dataset = read_csv('data/%s-feat.csv' % id, header=0, index_col=0)

n_features = dataset.shape[1]-1
train_split = 0.8
target = 'target'

print('n_features: %s ' % n_features)

values = dataset.values

X = values[:-1,:-1]
Y = values[1:,-1]

# make target column boolean
Y = Y > 0.0
print('market going up   %s times in dataset' % np.sum(Y))
print('market going down %s times in dataset' % np.sum(np.ones(len(Y)) - Y))

# split into train and test sets
n_train = int(values.shape[0] * train_split)

# split into input and outputs
train_X, train_y = X[:n_train,:], Y[:n_train]
test_X, test_y = X[n_train:,:], Y[n_train:]

C_candidates = expon.rvs(size=50, scale=100)
g_candidates = expon.rvs(size=50, scale=0.01)

param_grid = [
  {'C': C_candidates, 'gamma': g_candidates, 'kernel': ['rbf']}
]

clf = GridSearchCV(SVC(probability=True, tol=0.00000001), param_grid, cv=2,
                       scoring='accuracy')

model = clf.fit(train_X, train_y)
print("Best parameters set found on development set:")
print(clf.best_params_)
print("Grid scores on development set:")
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']

# Final performace metrics
pred_probs = clf.predict_proba(test_X)
preds = np.argmax(pred_probs, axis=-1)
print(test_y.astype(int))
print(preds)
accuracy = (preds == test_y).sum() / preds.shape[0]
print('accuracy test set: %s ' % accuracy)
