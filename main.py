# main.py

import time
import logging
import pandas as pd
from config import API_KEY, API_SECRET, TRADING_PAIR, TIMEFRAME, POSITION_SIZE
from model import train_model, predict_price
from utils.risk_management import check_daily_loss, calculate_position_size
from utils.indicators import rsi, macd
import ccxt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("forex_trading_bot.log"),
        logging.StreamHandler()
    ]
)

# Initialize the exchange API
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET
})

def fetch_data():
    """ Fetch data from an exchange. Handles errors during API interaction. """
    try:
        logging.info(f"Fetching data for {TRADING_PAIR} on timeframe {TIMEFRAME}...")
        data = exchange.fetch_ohlcv(TRADING_PAIR, timeframe=TIMEFRAME)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        logging.info(f"Successfully fetched {len(df)} records of data.")
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

def run_trading_bot():
    """ Main function to run the trading bot with error handling and decision making. """
    try:
        # Fetch market data
        data = fetch_data()
        if data is None:
            return  # Exit if data fetching failed
        
        # Train the model
        model, scaler = train_model(data)

        # Calculate technical indicators
        macd_values, macd_signal = macd(data)
        rsi_values = rsi(data)

        # Log technical indicator values
        logging.info(f"RSI: {rsi_values[-1]}, MACD: {macd_values[-1]}, MACD Signal: {macd_signal[-1]}")

        # Decision making: Buy or sell based on strategy
        position_size = calculate_position_size(balance=10000, risk_percentage=1, stop_loss_pips=50)

        # Define trading conditions for buying and selling
        if rsi_values[-1] < 30 and macd_values[-1] > macd_signal[-1]:
            logging.info(f"Buy signal detected for {TRADING_PAIR}. Buying {position_size} lots.")
            # Execute buy order
            execute_trade('buy', position_size)

        elif rsi_values[-1] > 70 and macd_values[-1] < macd_signal[-1]:
            logging.info(f"Sell signal detected for {TRADING_PAIR}. Selling {position_size} lots.")
            # Execute sell order
            execute_trade('sell', position_size)

        else:
            logging.info(f"No clear trade signal detected. Skipping trade...")

    except Exception as e:
        logging.error(f"Error in running trading bot: {e}")

def execute_trade(action, position_size):
    """ Execute trade action with error handling. """
    try:
        if action == 'buy':
            logging.info(f"Executing Buy order for {position_size} lots...")
            # Add the actual API call to execute a buy order
            exchange.create_market_buy_order(TRADING_PAIR, position_size)
            logging.info("Buy order executed successfully.")
        
        elif action == 'sell':
            logging.info(f"Executing Sell order for {position_size} lots...")
            # Add the actual API call to execute a sell order
            exchange.create_market_sell_order(TRADING_PAIR, position_size)
            logging.info("Sell order executed successfully.")
        
    except Exception as e:
        logging.error(f"Error executing {action} order: {e}")

# Run the bot every minute
if __name__ == "__main__":
    while True:
        run_trading_bot()
        time.sleep(60)  # Sleep for 60 seconds before the next trade decision
