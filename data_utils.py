import pandas as pd
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
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))  # Reshape for LSTM input
    return x, scaler
