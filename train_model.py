# train_model.py
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import joblib
from data_collection import collect_data
from config import TRADING_PAIR, DATA_PERIOD, DATA_INTERVAL

# Function to preprocess the data for model training
def preprocess_data(df):
    """
    Preprocess the collected data to be used for training the deep learning model.
    
    :param df: The raw historical data (e.g., from Forex market).
    :return: Preprocessed data ready for training.
    """
    # Ensure the 'Close' price is available in the dataframe
    if 'Close' not in df.columns:
        raise ValueError("Dataframe must contain 'Close' column.")

    # Use only the 'Close' prices for the model (for simplicity)
    close_prices = df['Close'].values

    # Scale the data using MinMaxScaler (to scale between 0 and 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    close_prices_scaled = scaler.fit_transform(close_prices.reshape(-1, 1))

    # Prepare the dataset for supervised learning (use previous 60 timesteps to predict the next one)
    X, y = [], []
    for i in range(60, len(close_prices_scaled)):
        X.append(close_prices_scaled[i-60:i, 0])  # Previous 60 timesteps
        y.append(close_prices_scaled[i, 0])      # Next timestep (the target)

    X = np.array(X)
    y = np.array(y)

    # Reshape X for LSTM input format (samples, timesteps, features)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    return X, y, scaler

# Define the deep learning model (LSTM in this case)
def build_model(input_shape):
    """
    Build and compile the LSTM model for time-series prediction.

    :param input_shape: Shape of the input data.
    :return: Compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=1))  # Output layer with one value (next close price)

    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

    return model

# Train the model and save it to a file
def train_and_save_model():
    """
    Train the deep learning model on historical data and save the trained model.
    """
    # Collect historical data (e.g., last 1 year of EURUSD data)
    df = collect_data(symbol=TRADING_PAIR, period=DATA_PERIOD, interval=DATA_INTERVAL)
    if df is None or df.empty:
        raise ValueError("No data found or data is empty. Cannot proceed with training.")

    # Preprocess the data for LSTM training
    X, y, scaler = preprocess_data(df)

    # Build the LSTM model
    model = build_model((X.shape[1], 1))

    # Train the model
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)  # You can increase epochs for better training

    # Save the trained model to a file
    model.save('model/deep_learning_model.h5')
    print("Model trained and saved successfully!")

    # Optionally, save the scaler (to be used for prediction later)
    # This helps in scaling new incoming data during prediction phase
    import joblib
    joblib.dump(scaler, 'model/scaler.pkl')

if __name__ == "__main__":
    train_and_save_model()
