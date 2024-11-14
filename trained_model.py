import tensorflow as tf
from model import build_model
from data_utils import preprocess_data
from config import DATA_SOURCE, TIMEFRAME
import api_utils

def train_model(symbol):
    # Fetch historical data
    data = api_utils.get_crypto_data(symbol, TIMEFRAME)
    if data:
        X, y, scaler = preprocess_data(data)
        
        # Split data into train/test
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # Build and train model
        model = build_model((X_train.shape[1], X_train.shape[2]))
        model.fit(X_train, y_train, epochs=50, batch_size=32)
        
        # Save trained model
        model.save('trading_model.h5')
        print("Model training complete.")
        return model, scaler
    else:
        print("Failed to retrieve data for training.")
        return None, None

def predict_price(model, data, scaler):
    # Preprocess the data
    X, _, _ = preprocess_data(data)
    
    # Predict the next price
    prediction = model.predict(X[-1].reshape(1, X.shape[1], X.shape[2]))
    prediction = scaler.inverse_transform(prediction)
    
    return prediction[0][0]
