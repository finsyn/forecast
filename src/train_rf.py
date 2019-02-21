import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from pandas import read_csv
from scipy.stats import binom_test
from os import environ, getenv
from sklearn.feature_selection import SelectKBest, f_classif

# reproducable results
np.random.seed(1337)

id = environ['TARGET_CFD_ID']
n_top_features = int(getenv('TRAIN_FEATURES', 15))
train_split = float(getenv('TRAIN_RATIO', 0.7))

dataset = read_csv('data/%s-feat.csv' % id, header=0, index_col=0)
values = dataset.values

X = values[:-1,:-1]
Y = values[1:,-1]

# Only use the best features
n_features = n_top_features
f_select = SelectKBest(f_classif, k=n_features)
X = f_select.fit_transform(X, Y)
f_top_idx = np.argsort(f_select.scores_)[-n_features:]
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

# train model
clf = RandomForestClassifier(
    n_estimators=300,
    # min_samples_split=50,
    criterion='gini',
    class_weight='balanced',
    max_depth=3
)
clf.fit(train_X, train_y)

pred_y = clf.predict(test_X)
pred_y_prob = clf.predict_proba(test_X)
conf_idx = np.any(pred_y_prob > 0.65, axis=1)
p = binom_test(np.sum(test_y == pred_y), len(test_y))

# print outcomes
print(dataset)
print(test_y)
print(pred_y)
# Get accuracy on test set
score = accuracy_score(test_y, pred_y) 
score_conf = accuracy_score(test_y[conf_idx], pred_y[conf_idx]) 
n_test = test_y.shape[0]
n_train = train_y.shape[0]
conf_ratio = np.sum(conf_idx)/n_test
print('n-train\t: %s' % n_train) 
print('n-test\t: %s' % n_test) 
print('p-value\t: %s' % p)
print('acc\t: %s' % score)
print('accconf\t: %s' % score_conf)
print('confrat\t: %s' % conf_ratio)

# Persist model
from joblib import dump
dump(clf, 'model-rf.joblib')
# save chosen features that are features in the trained model
np.savetxt(
    "outputs/%s-features.csv" % id,
    np.column_stack((f_top, f_top_idx)),
    delimiter=",",
    fmt="%s")


