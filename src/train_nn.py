import numpy as np
import sys
from pandas import read_csv
from scipy.stats import binom_test
from performance import confident_precision
from parse import get_train_data
from os import environ

np.random.seed(1337)

from keras.models import Input, Model
from keras.layers import LSTM, Dense, BatchNormalization, Activation, Dropout, Embedding, merge
from keras.layers.core import *
from keras.utils import to_categorical
from keras.optimizers import Adam, SGD

from keras.backend import argmax

from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix

id = environ['TARGET_CFD_ID']

dataset = read_csv('data/%s-feat.csv' % id, header=0, index_col=0)

n_features = dataset.shape[1]-1
n_output = 2
n_epochs = 300
train_split = 0.8
target = 'target'

print('n_features: %s ' % n_features)

print(dataset)

values = dataset.values

X = values[:-1,:-1]
Y = values[1:,-1]

# Only use the best features
n_features = 4
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

def omxmodel (n_features, n_values):

    inputs = Input(shape=(n_features,))

    X = Dense(units=6, activation='relu')(inputs)
    X = Dense(units=3, activation='relu')(X)
    predictions = Dense(n_values, activation='softmax')(X)

    model = Model(inputs=inputs, outputs=predictions)

    return model

# onetrain hot encode target column
train_y_oh = to_categorical(train_y, num_classes=n_output)
test_y_oh  = to_categorical(test_y , num_classes=n_output)

model = omxmodel(n_features, n_output)

print(model.summary())

optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=True)

# build network
model.compile(
        loss='binary_crossentropy',
        metrics=['accuracy'],
        optimizer=optimizer)

# fit network
history = model.fit(
        train_X, train_y_oh,
        epochs=n_epochs, batch_size=4,
        validation_data=(test_X, test_y_oh),
        shuffle=False)

# performace metrics
result = model.evaluate(test_X, test_y_oh, verbose=0)
if result:
    print('Test set mean absolute error: %s' % result[1])

# save model
model.save('outputs/%s-model.h5' % id)

# save history
np.savetxt(
        "data/%s-results.csv" % id,
        np.asarray([ history.history['loss'], history.history['val_loss']]),
        delimiter=",")

test_y_prob = model.predict(test_X)

# get actual predictions
test_y_pred = np.argmax(test_y_prob, axis=-1)

print('Test set confusion matrix:')
print(confusion_matrix(test_y, test_y_pred))
print('Test set p-value:')
print(binom_test(np.sum(test_y == test_y_pred), len(test_y)))

# save test output for simulations etc.
np.savetxt(
        "data/%s-test-output.csv" % id,
        np.asarray([ test_y_pred, test_y ]),
        delimiter=",")

confidence = np.amax(test_y_prob*10,axis=1).astype(int)
test_y_conf_pred = test_y_pred[confidence > 5]
test_y_conf_real = test_y[confidence > 5]
correct_confident = np.sum(test_y_conf_pred == test_y_conf_real)
n_confident = len(test_y_conf_pred)
acc_confident = correct_confident / n_confident
p_val_confident = binom_test(correct_confident, n_confident)


print('Test set all:')
print(test_y.astype(int))
print(test_y_pred)
print(confidence)
print('Test set confident accuracy: %s' % acc_confident)
print(confusion_matrix(test_y_conf_real, test_y_conf_pred))
print('Test set confident p-value: %s' % p_val_confident)
