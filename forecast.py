import numpy as np
import sys
from pandas import read_csv
from scipy import signal
from performance import confident_precision
from parse import get_train_data

from keras.models import Input, Model
from keras.layers import LSTM, Dense, BatchNormalization, Activation, Dropout
from keras.utils import to_categorical
from keras.backend import argmax

from matplotlib import pyplot

from sklearn import preprocessing
from sklearn.metrics import average_precision_score

n_lags = 9 
dataset = read_csv('omx-no-label.csv', header=0, index_col=0)
data = get_train_data(dataset, target='nordeaChange', n_lags=n_lags)
values = data.values

# normalize per feature
values[:,:-1] = preprocessing.scale(values[:,:-1])

# split into train and test sets
n_train = int(values.shape[0] * 0.8) 
train = values[:n_train, :]
test = values[n_train:, :]

# split into input and outputs
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

print(train_X[0,:])
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

def omxmodel (n_inputs, n_features, n_values):

    inputs = Input(shape=(n_inputs, n_features))

    # X = LSTM(64, return_sequences=True)(inputs)
    # X = Dense(n_features)(X)
    # X = Dropout(0.5)(X)
    X = LSTM(64)(inputs)
    X = Dense(n_features)(X)
    X = Dropout(0.4)(X)
    predictions = Dense(n_values)(X)

    model = Model(inputs=inputs, outputs=predictions)

    return model

model = omxmodel(train_X.shape[1], train_X.shape[2], 1)

print(model.summary())

# build network
model.compile(
        loss='mean_squared_error',
        metrics=['mae'],
        optimizer='adam')

# fit network
history = model.fit(
        train_X, train_y,
        epochs=5000, batch_size=32,
        validation_data=(test_X, test_y),
        shuffle=False)

# performace metrics
result = model.evaluate(test_X, test_y, verbose=0)
print('Test set mean absolute error: %s' % result[1])

# save model
model.save('model.h5')

# plot history
pyplot.figure()
pyplot.subplot(2, 1, 1)
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()

test_output = model.predict(test_X)
pred = test_output.reshape(len(test_y))

print('Test set all:')
print(np.around(test_y, 1))
print(np.around(pred, 1))

pyplot.subplot(2, 1, 2)
pyplot.plot(range(len(pred)), test_y, 'r', pred, 'b')
pyplot.show()
