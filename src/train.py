import numpy as np
import sys
from pandas import read_csv
from scipy.stats import binom_test
from performance import confident_precision
from parse import get_train_data

np.random.seed(1337)

from keras.models import Input, Model
from keras.layers import LSTM, Dense, BatchNormalization, Activation, Dropout, Embedding, merge
from keras.layers.core import *
from keras.utils import to_categorical
from keras.optimizers import Adam 
from keras.backend import argmax

from matplotlib import pyplot

from sklearn import preprocessing
from sklearn.metrics import average_precision_score, precision_recall_curve, confusion_matrix

dataset = read_csv('data/training.csv', header=0, index_col=0)

n_features = dataset.shape[1]
n_lags = 254
n_output = 2
n_epochs = 90
train_split = 0.8
target = 'target'

print('n_features: %s ' % n_features)
print('n_lags: %s ' % n_lags)

data = get_train_data(dataset, target=target, n_lags=n_lags)

values = data.values

X = values[:,:-1]
Y = values[:,-1]

# make target column boolean
Y = Y > 0.0
print('market going up   %s times in dataset' % np.sum(Y))
print('market going down %s times in dataset' % np.sum(np.ones(len(Y)) - Y))

# split into train and test sets
n_train = int(values.shape[0] * train_split) 

# split into input and outputs
train_X, train_y = X[:n_train,:], Y[:n_train]
test_X, test_y = X[n_train:,:], Y[n_train:]

# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_lags, n_features))
test_X = test_X.reshape((test_X.shape[0], n_lags, n_features))

print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

def omxmodel (n_inputs, n_features, n_values):

    inputs = Input(shape=(n_inputs, n_features))

    # X = LSTM(16, return_sequences=True)(inputs)
    # X = Dropout(0.5)(X)
    X = LSTM(2)(inputs)
    # X = Dropout(0.8)(X)
    # X = Dense(units=8, activation='relu')(X)
    # X = Dropout(0.5)(X)
    predictions = Dense(n_values, activation='softmax')(X)

    model = Model(inputs=inputs, outputs=predictions)

    return model

# onetrain hot encode target column
train_y_oh = to_categorical(train_y, num_classes=n_output)
test_y_oh  = to_categorical(test_y , num_classes=n_output)

model = omxmodel(n_lags, n_features, n_output)

print(model.summary())

# build network
model.compile(
        loss='binary_crossentropy',
        metrics=['accuracy'],
        optimizer='adam')

# fit network
history = model.fit(
        train_X, train_y_oh,
        epochs=n_epochs, batch_size=32,
        validation_data=(test_X, test_y_oh),
        shuffle=False)

# performace metrics
result = model.evaluate(test_X, test_y_oh, verbose=0)
print('Test set mean absolute error: %s' % result[1])

# save model
model.save('model.h5')

# plot history
pyplot.figure()
pyplot.subplot(2, 1, 1)
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()

test_y_prob = model.predict(test_X)

avg_precision = average_precision_score(test_y_oh, test_y_prob) 
print('Test set average precision score: %s' % avg_precision)
# get actual predictions
test_y_pred = np.argmax(test_y_prob, axis=-1) 

print('Test set confusion matrix:')
print(confusion_matrix(test_y, test_y_pred))
print('Test set p-value:')
print(binom_test(np.sum(test_y == test_y_pred), len(test_y)))

# save test output for simulations etc.
np.savetxt(
        "data/test-output.csv",
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

pyplot.show()
