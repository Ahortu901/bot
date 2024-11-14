import pandas as pd
import numpy as np
from trained_model import predict_price
from data_utils import preprocess_data
from risk_management import calculate_position_size
from datetime import datetime

def backtest_strategy(symbol, model, scaler, data, initial_balance=10000, transaction_fee=0.001):
    """
    Backtest the strategy using historical data.

    Args:
    - symbol (str): Trading pair symbol.
    - model (tensorflow.keras.Model): The trained model to predict prices.
    - scaler (MinMaxScaler): The scaler used to normalize the price data.
    - data (list): Historical market data.
    - initial_balance (float): The starting balance for the backtest.
    - transaction_fee (float): The fee deducted per trade.

    Returns:
    - pd.DataFrame: A DataFrame containing the balance and positions over time.
    """
    # Preprocess the data
    X, y, _ = preprocess_data(data)
    
    # Initialize portfolio and variables
    balance = initial_balance
    position_size = 0
    position = None
    portfolio_balance = [balance]
    positions = []
    entry_price = 0

    for i in range(len(X)):
        # Predict the next price
        predicted_price = predict_price(model, data[i:i+1], scaler)
        
        # Risk management and position sizing
        if position is None:  # No open position
            position_size = calculate_position_size(balance, predicted_price, predicted_price * 0.98)
            positions.append({"timestamp": data[i]['timestamp'], "action": "BUY", "price": predicted_price, "quantity": position_size})
            balance -= position_size * predicted_price * (1 + transaction_fee)
            position = "long"
            entry_price = predicted_price
        else:
            # Example strategy: Sell if price goes up by 2% or down by 2%
            if predicted_price >= entry_price * 1.02:  # Take profit
                positions.append({"timestamp": data[i]['timestamp'], "action": "SELL", "price": predicted_price, "quantity": position_size})
                balance += position_size * predicted_price * (1 - transaction_fee)
                position = None  # Position closed
            elif predicted_price <= entry_price * 0.98:  # Stop loss
                positions.append({"timestamp": data[i]['timestamp'], "action": "SELL", "price": predicted_price, "quantity": position_size})
                balance += position_size * predicted_price * (1 - transaction_fee)
                position = None  # Position closed

        # Record balance over time
        portfolio_balance.append(balance + (position_size * predicted_price if position == "long" else 0))

    # Create a DataFrame for analysis
    result = pd.DataFrame(positions)
    result['portfolio_balance'] = portfolio_balance[1:]
    return result
