import time
import numpy as np
from trained_model import train_model, predict_price
from api_utils import get_crypto_data, place_order
from risk_management import calculate_position_size
from config import API_KEY, API_SECRET
from backtest import backtest_strategy
import pandas as pd


def run_backtest(symbol, model, scaler):
    """Run backtest with historical data."""
    data = get_crypto_data(symbol, "1h", limit=1000)
    if not data:
        print("Failed to fetch data for backtest.")
        return
    
    backtest_result = backtest_strategy(symbol, model, scaler, data)
    
    # Output the backtest results
    print("Backtest completed.")
    print(backtest_result.tail())  # Show the final few trades and portfolio balance
    return backtest_result


def run_bot(symbol):
    model, scaler = train_model(symbol)
    if model is None:
        print("Model training failed. Exiting.")
        return
    
    mode = input("[-] Enter 'Live' for paper traiding or 'backtesting' for backtesting: ")

    if mode == 'live':
    # Fetch initial data
        data = get_crypto_data(symbol, "1h", limit=1000)
        if data is None:
            print("Failed to fetch data. Exiting.")
            return
        
        # Initialize balance and position
        portfolio_balance = 10000  # Example starting balance (USD)
        position = None
        
        while True:
            # Predict the next price movement
            predicted_price = predict_price(model, data, scaler)
            print(f"Predicted next price for {symbol}: {predicted_price}")
            
            # Risk management & position sizing
            if position is None:  # No active position
                position_size = calculate_position_size(portfolio_balance, predicted_price, predicted_price * 0.98)
                print(f"Calculated position size: {position_size}")
                place_order(symbol, "BUY", position_size, predicted_price)
                position = "long"
            else:  # If there's an open position, we should handle it
                # Example: If price moves up by 2%, take profit
                if predicted_price > 1.02 * predicted_price:  # Adjust the condition as needed
                    place_order(symbol, "SELL", position_size, predicted_price)
                    position = None
            
            # Wait before next prediction
            time.sleep(3600)  # Wait for the next hour
            
    elif mode == 'backtest':
        run_backtest(symbol, model, scaler)
    else:
        print("[+] Invalid mode. Exiting.")

if __name__ == "__main__":
    symbol = "BTC_USDT"
    run_bot(symbol)
