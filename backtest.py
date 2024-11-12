# backtest.py
import pandas as pd
import numpy as np
import joblib
import logging
from calculate_sharpe_ratio import calculate_sharpe_ratio
from data_collection import collect_data
from config import TRADING_PAIR, DATA_PERIOD, DATA_INTERVAL


# Load the trained model and scaler
model = load_model('model/deep_learning_model.h5')
scaler = joblib.load('model/scaler.pkl')

# Simulate a new data point (e.g., the latest 60 timesteps)
new_data = np.array([0.0] * 60)  # Replace with actual latest 60 closing prices

# Rescale the data using the same scaler
new_data_scaled = scaler.transform(new_data.reshape(-1, 1))

# Reshape data for LSTM input
new_data_scaled = new_data_scaled.reshape((1, 60, 1))

# Make a prediction (next closing price)
predicted_price = model.predict(new_data_scaled)
predicted_price = scaler.inverse_transform(predicted_price)  # Inverse scale to original value

print(f"Predicted Next Closing Price: {predicted_price}")

def backtest_strategy():
    """
    Backtest the trading strategy and calculate performance metrics like Sharpe ratio.
    """
    logging.info("Starting backtest...")

    try:
        # Simulate historical trading data or collect actual trading data
        df = collect_data(symbol=TRADING_PAIR, period=DATA_PERIOD, interval=DATA_INTERVAL)

        # Simulated returns for backtesting purposes (Replace with actual strategy results)
        # Assuming these are daily returns (percentage change) based on the strategy's performance
        df['Returns'] = df['Close'].pct_change()

        # Calculate Sharpe ratio for the strategy returns
        sharpe_ratio = calculate_sharpe_ratio(df['Returns'])

        logging.info(f"Sharpe Ratio of the strategy: {sharpe_ratio:.4f}")

    except Exception as e:
        logging.error(f"Error in backtesting: {e}")
