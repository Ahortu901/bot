# trade.py
import logging
import time
from tensorflow.keras.models import load_model
import joblib
import numpy as np

from calculate_sharpe_ratio import calculate_sharpe_ratio
from data_collection import collect_data
from config import TRADING_PAIR, INTERVAL, DATA_PERIOD, DATA_INTERVAL, API_KEY, SECRET_KEY


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
# Simulated function to fetch account balance (replace with actual API if using a broker)
def get_account_balance():
    """Fetch account balance (simulated). In real case, this would be an API call."""
    return 10000  # Example: $10,000 account balance

# Function to calculate position size based on account balance and risk
def calculate_position_size(account_balance, stop_loss_distance, risk_percentage=0.01):
    """Calculate the position size based on account balance, stop-loss, and risk percentage."""
    risk_per_trade = account_balance * risk_percentage
    position_size = risk_per_trade / stop_loss_distance
    return position_size

# Function to calculate stop-loss and take-profit levels
def calculate_exit_levels(entry_price, stop_loss_percentage=0.02, take_profit_percentage=0.04):
    """Calculate the stop-loss and take-profit levels."""
    stop_loss_level = entry_price * (1 - stop_loss_percentage)
    take_profit_level = entry_price * (1 + take_profit_percentage)
    return stop_loss_level, take_profit_level

# Simulated trade execution function
def execute_trade(signal, account_balance, entry_price):
    """Execute buy/sell action based on the model's prediction with risk management."""
    if signal == 1:
        logging.info("Executing Buy Order!")

        # Calculate stop-loss, take-profit, and position size
        stop_loss_level, take_profit_level = calculate_exit_levels(entry_price)
        stop_loss_distance = entry_price - stop_loss_level
        position_size = calculate_position_size(account_balance, stop_loss_distance)

        logging.info(f"Stop-Loss Level: {stop_loss_level}, Take-Profit Level: {take_profit_level}")
        logging.info(f"Position Size: {position_size:.2f} units")

        # Place order (simulation)
        # broker_api.buy(TRADING_PAIR, position_size)

    elif signal == -1:
        logging.info("Executing Sell Order!")

        # Calculate stop-loss, take-profit, and position size
        stop_loss_level, take_profit_level = calculate_exit_levels(entry_price)
        stop_loss_distance = entry_price - stop_loss_level
        position_size = calculate_position_size(account_balance, stop_loss_distance)

        logging.info(f"Stop-Loss Level: {stop_loss_level}, Take-Profit Level: {take_profit_level}")
        logging.info(f"Position Size: {position_size:.2f} units")

        # Place order (simulation)
        # broker_api.sell(TRADING_PAIR, position_size)

    else:
        logging.info("No action taken. Hold position.")

# Main function to run trading logic with risk management
def trade_forex():
    """Main trading logic with risk management features."""
    logging.info("Starting the trading process...")

    try:
        # Collect the latest market data
        df = collect_data(symbol=TRADING_PAIR, period=DATA_PERIOD, interval=DATA_INTERVAL)
        
        # Calculate Sharpe ratio for the strategy returns
        sharpe_ratio = calculate_sharpe_ratio(df['Returns'])

        # Predict the signal (1 for Buy, 0 for Hold, -1 for Sell)
        signal = predict_signal(df)

        # Get account balance (simulated)
        account_balance = get_account_balance()

        # Get the latest market price (assumed to be the closing price)
        entry_price = df['Close'].iloc[-1]

        # Execute the trade with the calculated stop-loss, take-profit, and position size
        execute_trade(signal, account_balance, entry_price)

    except Exception as e:
        logging.error(f"Error during trading: {e}")
