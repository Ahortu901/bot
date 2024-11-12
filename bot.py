import time
import logging
from trader import execute_trade, get_balance
from model import train_model, predict_price
from strategy import advanced_strategy
from risk_management import manage_risk, apply_stop_loss_take_profit
from utils import fetch_data
from config import API_KEY, API_SECRET, SYMBOL, TIMEFRAME, LIMIT, RISK_PERCENTAGE, TRADE_AMOUNT, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE
from mining_model import MiningProfitabilityModel
from data_collector import DataCollector
import ccxt

# Initialize exchange client (e.g., Binance)
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# Initialize mining profitability model
mining_model = MiningProfitabilityModel()


def get_market_data():
    # Fetch real-time data (price of cryptocurrency, etc.)
    ticker = exchange.fetch_ticker(SYMBOL)
    return ticker['last']  # Example: last price of the cryptocurrency


def run_mining_operations():
    while True:
        try:
            # Get real-time market data (price)
            crypto_price = get_market_data()

            df = DataCollector.collect_data()

            # Extract the collected data
            crypto_price = df['crypto_price'].values[0]
            difficulty = df['mining_difficulty'].values[0]
            hash_rate = df['hash_rate'].values[0]
            energy_cost = df['energy_cost'].values[0]
            power_usage = df['power_usage'].values[0]

            # Use the mining model to predict profitability
            profitability = mining_model.predict_profitability(difficulty, hash_rate, energy_cost, crypto_price, power_usage)
            print(f"Predicted mining profitability: {profitability:.4f}")

            # If profitability is positive, execute some mining strategy (this is a placeholder)
            if profitability > 0.05:
                print("Mining operation is profitable! Start mining...")
            else:
                print("Mining is not profitable, pausing operations.")

            # Sleep for some time before recalculating
            time.sleep(3600)  # Example: run every hour

        except Exception as e:
            print(f"Error during mining operations: {e}")
            time.sleep(60)  # Retry after a short delay

def run():
    model = train_model('data/data_collected.csv')  # Load trained model
    while True:
        try:
            df = fetch_data(exchange, SYMBOL, TIMEFRAME, LIMIT)
            prediction = predict_price(model, df)

            # Apply advanced strategy (e.g., trend-following, mean-reversion)
            action, entry_price = advanced_strategy(prediction, df)

            if action:
                # Check risk management and execute trade
                manage_risk(exchange, SYMBOL, action, RISK_PERCENTAGE)
                execute_trade(exchange, action, SYMBOL, TRADE_AMOUNT)

                # Apply stop-loss and take-profit strategy
                apply_stop_loss_take_profit(exchange, SYMBOL, entry_price, action, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE)
            
            time.sleep(60 * 60)  # Wait for 1 hour

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    run()
