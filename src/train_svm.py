from __future__ import division

import numpy as np
import sys
from pandas import read_csv
from scipy.stats import binom_test, expon, chi
from os import environ

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

id = environ['TARGET_CFD_ID']

dataset = read_csv('data/%s-feat.csv' % id, header=0, index_col=0)

n_features = dataset.shape[1]-1
n_models = 10
n_outputs = 2
# we can increase num of CV folds once we have more data
# but now the validation set will be too small if cv is larger
n_folds = 2
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

# Train multiple models to get a more stable final prediction
models = []
all_pred = np.zeros((len(test_y), n_models))
print('### Finding %s models' % n_models)
for i in range(0, n_models):
    # C_candidates = expon.rvs(size=10, scale=100)
    C_candidates = np.random.uniform(0.0, 1e9, 10)
    # g_candidates = expon.rvs(size=10, scale=0.0001)
    g_candidates = np.random.uniform(1e-10, 0.0, 10) 

    param_grid = [
        {'C': C_candidates, 'gamma': g_candidates, 'class_weight': ['balanced', None], 'kernel': ['rbf']}
    ]

    clf = GridSearchCV(
        SVC(
            tol=1e-3,
            shrinking=True,
            verbose=False
        ),
        param_grid,
        cv=n_folds,
        scoring='accuracy'
    )
    clf.fit(train_X, train_y)
    print("### Best parameters set found on development set (iter %s):" % i)
    print(clf.best_params_)

    all_pred[:,i] = clf.predict(test_X)

    models.append(clf)


print(all_pred)
# Get mean prediction of all models per sample
pred = (np.mean(all_pred, -1) > 0.5).astype(int)
print('### Predictions on test set')
print(test_y.astype(int))
print(pred)
accuracy = (pred == test_y).sum() / pred.shape[0]
print('accuracy test set: %s ' % accuracy)
