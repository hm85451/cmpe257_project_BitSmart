# -*- coding: utf-8 -*-
"""Copy of BTC_USD_LSTM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s1iRW8rW5v-iQQYB4PkH2y3wE0m1FCpc
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Bidirectional
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


# Create sequences of data for LSTM model
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

# Load the dataset
data = pd.read_csv('../data/BTC-USD.csv')

# Select relevant features
features = ['Open', 'High', 'Low', 'Close','Volume']
data = data[features]

# Preprocess the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Split the data into training and testing sets
training_size = int(len(scaled_data) * 0.99)
train_data = scaled_data[:training_size]
test_data = scaled_data[training_size:]

seq_length = 60
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=len(features)))

# Commented out IPython magic to ensure Python compatibility.
# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')
# %tensorflow_version 2.x
import tensorflow as tf
with tf.device('/device:GPU:0'):
  # Train the model
  model.fit(X_train, y_train, epochs=5, batch_size=32)

test_data = scaled_data[training_size-120:]
X_test, y_test = create_sequences(test_data, seq_length)

# Make predictions
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

x_f = np.delete(X_test[94], (0), axis=0)

x_f = np.vstack([x_f,predictions[94]])

# x_f.shape

pred = model.predict(x_f.reshape((1,60,5)))
pred = scaler.inverse_transform(pred)

# predictions[94]

# pred

# # Visualize the results
# plt.figure(figsize=(10, 6))
# plt.plot(data.index[training_size-120+seq_length:], data['Close'][training_size-120+seq_length:], label='Actual Close Price')
# plt.plot(data.index[training_size-120+seq_length:], predictions[:, 3], label='Predicted Close Price')
# plt.xlabel('Date')
# plt.ylabel('BTC-USD Price (USD)')
# plt.title('BTC-USD Price Prediction using LSTM')
# plt.grid()
# plt.legend()
# plt.show()

def InputValue(x,pred):
  x_f = np.delete(x, (0), axis=0)
  x_f = np.vstack([x_f,pred])
  return x_f

x_feature = InputValue(X_test[94],predictions[94])

x_feature.shape

pred = predictions[94]
N=10
N_predictions=[]
N_predictions.append(np.array(pred).reshape(len(features)))
for _ in range(N):
  pred = model.predict(x_feature.reshape((1,seq_length,len(features))))
  pred = scaler.inverse_transform(pred)
  N_predictions.append(np.array(pred).reshape(len(features)))
  x_feature = InputValue(x_feature,pred)

# N_predictions

# predictions[94]

# X_test[93].shape

# plt.figure(figsize=(10, 5))
# plt.plot(np.array(N_predictions)[:, 3], label='Predicted Close Price')
# plt.xlabel('Date')
# plt.ylabel('BTC-USD Price (USD)')
# plt.title('BTC-USD Price Prediction using LSTM')
# plt.grid()
# plt.legend()
# plt.show()

model.save('../btc_usd_lstm.keras')

model.save('../btc_usd_lstm.h5')