from __future__ import division

import numpy as np
import sys
from pandas import read_csv
from scipy.stats import binom_test, expon, chi, gamma
from os import environ

from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

id = environ['TARGET_CFD_ID']
f_n = environ['TRAIN_FEATURES']

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

# Only use the best features
f_select = SelectKBest(f_classif, k=f_n)
X = f_select.fit_transform(X, Y)
f_top_idx = np.argsort(f_select.scores_)[-f_n:]
f_top = np.take(dataset.columns.values, f_top_idx)

print('### Selected features')
print('\n'.join(f_top))

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
    rC = np.random.rand() + 8
    rg = np.random.rand() + 8 
    C_candidates = expon.rvs(size=10, scale=np.power(10,rC))
    g_candidates = expon.rvs(size=10, scale=np.power(10,-rg))

    param_grid = [
        {'C': C_candidates, 'gamma': g_candidates, 'class_weight': ['balanced', None], 'kernel': ['rbf']}
    ]

    clf = GridSearchCV(
        SVC(
            tol=1e-4,
            # shrinking=True,
            max_iter=1e7,
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

# Get mean prediction of all models per sample
pred_prob = np.mean(all_pred, -1)
print('### Probabilites on test set')
print(pred_prob)
pred = (pred_prob > 0.5).astype(int)
print('### Predictions on test set')
print(test_y.astype(int))
print(pred)
accuracy = (pred == test_y).sum() / pred.shape[0]
print('accuracy test set: %s ' % accuracy)
