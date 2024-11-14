import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from config import WINDOW_SIZE

def preprocess_data(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    
    # Normalize data
    scaler = MinMaxScaler()
    df[['close']] = scaler.fit_transform(df[['close']])

    # Create windowed data for prediction
    X, y = [], []
    for i in range(len(df) - WINDOW_SIZE):
        X.append(df['close'].iloc[i:i + WINDOW_SIZE].values)
        y.append(df['close'].iloc[i + WINDOW_SIZE])

    X = np.array(X)
    y = np.array(y)
    return X, y, scaler
