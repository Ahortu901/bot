# model.py

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import TA_Lib as ta

def preprocess_data(data):
    """ Preprocess the Forex data for the model input. """
    # Use technical indicators like RSI, MACD, and moving averages
    data['RSI'] = ta.RSI(data['Close'], timeperiod=14)
    data['MACD'], data['MACD_signal'], _ = ta.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    data['SMA_50'] = ta.SMA(data['Close'], timeperiod=50)
    data['SMA_200'] = ta.SMA(data['Close'], timeperiod=200)

    # Use the close price for scaling
    close_prices = data[['Close']].values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)
    
    return scaled_data, scaler

def create_lstm_model(input_shape):
    """ Create and compile the LSTM model. """
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # Output layer for price prediction

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_price(model, data):
    """ Make a prediction with the trained model. """
    return model.predict(data)

def train_model(data):
    """ Train the LSTM model with the data. """
    scaled_data, scaler = preprocess_data(data)
    
    # Prepare data for LSTM
    X = []
    y = []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])
    
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM input

    # Create and train the model
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=50, batch_size=32)
    return model, scaler
