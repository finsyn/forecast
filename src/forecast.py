import numpy as np
import sys
from pandas import read_csv
from scipy import signal
from performance import confident_precision
from parse import get_train_data

from keras.models import Input, Model
from keras.layers import LSTM, Dense, BatchNormalization, Activation, Dropout, Embedding, merge
from keras.layers.core import *
from keras.utils import to_categorical
from keras.backend import argmax

from matplotlib import pyplot

from sklearn import preprocessing
from sklearn.metrics import average_precision_score, precision_recall_curve, confusion_matrix


dataset = read_csv('data/training.csv', header=0, index_col=0)

n_features = dataset.shape[1]
n_lags = 40 
n_output = 2
n_epochs = 150
train_split = 0.8
target = 'market-index_OMX30-c_2_o'
SINGLE_ATTENTION_VECTOR = False

print('n_features: %s ' % n_features)
print('n_lags: %s ' % n_lags)

data = get_train_data(dataset, target=target, n_lags=n_lags)

values = data.values

X = values[:,:-1]
Y = values[:,-1]

# normalize per feature
X = preprocessing.scale(X)

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

def attention_3d_block(inputs):
    # inputs.shape = (batch_size, time_steps, input_dim)
    input_dim = int(inputs.shape[2])
    a = Permute((2, 1))(inputs)
    a = Reshape((input_dim, n_lags))(a) # this line is not useful. It's just to know which dimension is what.
    a = Dense(n_lags, activation='softmax')(a)
    if SINGLE_ATTENTION_VECTOR:
        a = Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
        a = RepeatVector(input_dim)(a)
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
    return output_attention_mul

def omxmodel (n_inputs, n_features, n_values):

    inputs = Input(shape=(n_inputs, n_features))

    X = LSTM(128, return_sequences=True)(inputs)
    # attention_mul = attention_3d_block(lstm_out)
    # attention_mul = Flatten()(attention_mul)
    X = LSTM(128)(X)
    # X = Dense(128)(attention_mul)
    # X = Dropout(0.5)(X)
    # X = LSTM(256)(X)
    # X = Dense(n_features)(lstm_out)
    X = Dropout(0.5)(X)
    # regression or classification?
    # predictions = Dense(n_values)(attention_mul)
    predictions = Dense(n_values, activation='softmax')(X)

    model = Model(inputs=inputs, outputs=predictions)

    return model

# onetrain hot encode target column
train_y_oh = to_categorical(train_y, num_classes=n_output)
test_y_oh  = to_categorical(test_y , num_classes=n_output)

model = omxmodel(train_X.shape[1], n_features, n_output)

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

print('confusion matrix:')
print(confusion_matrix(test_y, test_y_pred))

# save test output for simulations etc.
np.savetxt(
        "data/test-output.csv",
        np.asarray([ test_y_pred, test_y ]),
        delimiter=",")

print('Test set all:')
print(test_y.astype(int))
print(test_y_pred)
print(np.amax(test_y_prob*10,axis=1).astype(int))

pyplot.show()
