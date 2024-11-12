# model.py
from keras.models import load_model
import logging
import pandas as pd
import numpy as np
import talib as ta

# Load the pre-trained model (ensure it's already trained and saved)
model = load_model('model.h5')

# Function to add technical indicators to the DataFrame
def add_technical_indicators(df):
    df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
    df['EMA_20'] = ta.EMA(df['Close'], timeperiod=20)
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['ATR'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    return df

# Preprocessing the data for the model
def preprocess_data(df):
    df = add_technical_indicators(df)
    features = ['SMA_50', 'EMA_20', 'RSI', 'MACD', 'ATR']
    df = df.dropna()  # Drop NaN values resulting from technical indicator calculations
    X = df[features].values
    return X

# Function to make predictions (Buy, Sell, Hold)
def predict_signal(df):
    try:
        X = preprocess_data(df)
        prediction = model.predict(X[-1:].reshape(1, -1))  # Predict on the most recent data point
        predicted_signal = np.argmax(prediction)  # Buy (1), Hold (0), Sell (-1)
        return predicted_signal
    except Exception as e:
        logging.error(f"Error predicting signal: {e}")
        raise
