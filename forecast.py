import numpy as np
from pandas import read_csv
from utils import series_to_supervised 
from keras.models import Input, Model
from keras.layers import LSTM, Dense, BatchNormalization, Activation, Dropout
from keras.utils import to_categorical
from keras.backend import argmax
from matplotlib import pyplot

dataset = read_csv('omx.csv', header=0, index_col=0)
values = dataset.values

# unique values in categorical output column
state_to_idx = {state: idx for idx, state in enumerate(list(set(values[:,-1])))}
n_output = len(state_to_idx)

# replace output column with index values
values[:,-1] = [state_to_idx[x] for x in values[:,-1]]

# frame as supervised learning
# with one time shift since we want to predict the following day
reframed = series_to_supervised(values, 30, 1)

# drop shifted columns we don't want to predict
# @TODO we currently feed in shifted label value as well
# reframed.drop(reframed.columns[[5,6]], axis=1, inplace=True)

# split into train and test sets
values = reframed.values
n_train = int(values.shape[0] * 0.8) 
train = values[:n_train, :]
test = values[n_train:, :]

# split into input and outputs
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

def omxmodel (n_inputs, n_features, n_values):

    inputs = Input(shape=(n_inputs, n_features))

    X = LSTM(64, return_sequences=True)(inputs)
    X = Dense(n_features)(X)
    X = Dropout(0.5)(X)
    X = LSTM(64)(X)
    X = Dense(n_features)(X)
    X = Dropout(0.5)(X)
    predictions = Dense(n_values, activation='softmax')(X)

    model = Model(inputs=inputs, outputs=predictions)

    return model

# one hot encode target column
train_y_oh = to_categorical(train_y, num_classes=n_output)
test_y_oh  = to_categorical(test_y , num_classes=n_output)

model = omxmodel(train_X.shape[1], train_X.shape[2], len(state_to_idx))

print(model.summary())

# build network
model.compile(
        loss='categorical_crossentropy',
        metrics=['accuracy'],
        optimizer='adam')

# fit network
history = model.fit(
        train_X, train_y_oh,
        epochs=1000, batch_size=32,
        shuffle=False)

result = model.evaluate(test_X, test_y_oh, verbose=0)
print('Test set accuracy: %s' % result[1])
