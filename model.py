import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

# Load forex data and preprocess
def load_forex_data(filepath, feature='Close'):
    data = pd.read_csv(filepath, date_parser=True)
    data = data[['Date', feature]]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data

# Preprocess data for prediction (use last `lookback` data points)
def preprocess_data_for_prediction(data, lookback=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    x = []
    x.append(scaled_data[-lookback:, 0])  # Use the last `lookback` data points
    x = np.array(x)
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))  # Reshape for GRU input
    return x, scaler

# Build and compile a fast GRU model
def build_gru_model(input_shape):
    model = Sequential()
    model.add(GRU(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(GRU(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # Output layer to predict next price
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Load pre-trained GRU model (or train it if needed)
def load_trained_model(model_path='gru_forex_model.h5'):
    model = build_gru_model(input_shape=(60, 1))  # Assuming 60 time-steps for prediction
    model.load_weights(model_path)
    return model

# Make prediction using the GRU model
def predict_next_price(model, data, lookback=60):
    x_input, scaler = preprocess_data_for_prediction(data, lookback)
    predicted_price = model.predict(x_input)
    predicted_price = scaler.inverse_transform(predicted_price)
    return predicted_price[0][0]
