import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def train_model(data_file):
    df = pd.read_csv(data_file)
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)  # Buy (1) or Sell (0)
    
    features = df[['open', 'high', 'low', 'close', 'volume']].dropna()
    target = df['target'].dropna()
    
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    
    X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=42)

    # Deep learning model (LSTM)
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, batch_size=1, epochs=5, verbose=1)

    # Evaluate model
    accuracy = model.evaluate(X_test, y_test)
    print(f"Model Accuracy: {accuracy[1]}")

    return model

def predict_price(model, df):
    features = df[['open', 'high', 'low', 'close', 'volume']].tail(1).values
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    features_scaled = features_scaled.reshape((features_scaled.shape[0], features_scaled.shape[1], 1))

    prediction = model.predict(features_scaled)
    return 'buy' if prediction[0] > 0.5 else 'sell'
