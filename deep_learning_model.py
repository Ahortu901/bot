import pandas as pd
import talib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Load Forex data
def load_data(file_name="historical_forex_data.csv"):
    df = pd.read_csv(file_name)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# Add technical indicators to the data
def add_technical_indicators(df):
    # Moving Averages
    df['SMA_14'] = talib.SMA(df['rate'], timeperiod=14)  # 14-period Simple Moving Average
    df['EMA_14'] = talib.EMA(df['rate'], timeperiod=14)  # 14-period Exponential Moving Average

    # Relative Strength Index (RSI)
    df['RSI_14'] = talib.RSI(df['rate'], timeperiod=14)  # 14-period RSI

    # Moving Average Convergence Divergence (MACD)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['rate'], fastperiod=12, slowperiod=26, signalperiod=9)

    # Bollinger Bands (BB)
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(df['rate'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    # Stochastic Oscillator
    df['STOCH_slowk'], df['STOCH_slowd'] = talib.STOCH(df['rate'], df['rate'], df['rate'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    # On-Balance Volume (OBV)
    df['OBV'] = talib.OBV(df['rate'], df['volume'])  # Assuming there is a 'volume' column

    # Average True Range (ATR)
    df['ATR'] = talib.ATR(df['high'], df['low'], df['rate'], timeperiod=14)

    # Parabolic SAR
    df['SAR'] = talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)

    # Remove rows with NaN values (which may appear due to technical indicators)
    df.dropna(inplace=True)
    
    return df

# Normalize the data using MinMaxScaler
def normalize_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    # We normalize only the numeric columns (features), excluding the date
    df_scaled = scaler.fit_transform(df)
    return df_scaled, scaler

# Create sequences of data for LSTM
def create_sequences(data, time_step=60):
    x_data, y_data = [], []

    for i in range(len(data) - time_step - 1):
        x_data.append(data[i:i + time_step])  # Sequence of past `time_step` values (all indicators)
        y_data.append(data[i + time_step, 0])  # Next value to predict (rate)

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Reshape X to be 3D for LSTM input: [samples, time steps, features]
    x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], x_data.shape[2]))

    return x_data, y_data

# Build and compile the LSTM model
def build_lstm_model(input_shape):
    model = Sequential()

    # LSTM layers with Dropout for regularization
    model.add(LSTM(units=100, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))  # Dropout layer to prevent overfitting
    model.add(LSTM(units=100, return_sequences=False))
    model.add(Dropout(0.2))  # Dropout layer to prevent overfitting

    # Fully connected layer to predict the next rate
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train the LSTM model
def train_model(x_train, y_train, x_test, y_test, epochs=10, batch_size=32):
    model = build_lstm_model((x_train.shape[1], x_train.shape[2]))

    # Train the model
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test))

    # Save the trained model
    model.save("forex_model_with_indicators.h5")
    
    return model

# Predict using the trained model
def predict(model, x_input):
    predictions = model.predict(x_input)
    return predictions

# Plot predictions vs actual values
def plot_predictions(y_test, predictions):
    plt.figure(figsize=(10,6))
    plt.plot(y_test, color='blue', label='Actual Exchange Rate')
    plt.plot(predictions, color='red', label='Predicted Exchange Rate')
    plt.title('Forex Rate Prediction vs Actual')
    plt.xlabel('Time')
    plt.ylabel('Exchange Rate')
    plt.legend()
    plt.show()

# Main function to execute the entire process
if __name__ == "__main__":
    # Load the Forex data (replace with your actual dataset)
    df = load_data("historical_forex_data.csv")

    # Add technical indicators to the data
    df_with_indicators = add_technical_indicators(df)

    # Normalize the data (scaling all features between 0 and 1)
    df_scaled, scaler = normalize_data(df_with_indicators)

    # Create sequences of data for LSTM model (using 60 time steps)
    time_step = 60
    x_data, y_data = create_sequences(df_scaled, time_step)

    # Split the data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, shuffle=False)

    # Train the LSTM model
    model = train_model(x_train, y_train, x_test, y_test, epochs=10)

    # Predict using the trained model
    predictions = predict(model, x_test)

    # Inverse transform the predictions and actual values to get the original scale
    predictions = scaler.inverse_transform(np.column_stack([predictions] * df_scaled.shape[1]))[:, 0]
    y_test_actual = scaler.inverse_transform(np.column_stack([y_test] * df_scaled.shape[1]))[:, 0]

    # Plot the predictions vs actual values
    plot_predictions(y_test_actual, predictions)
