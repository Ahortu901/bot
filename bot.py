import time
import logging
from trader import execute_trade, get_balance
from model import train_model, predict_price
from strategy import advanced_strategy
from risk_management import manage_risk, apply_stop_loss_take_profit
from utils import fetch_data
from config import API_KEY, API_SECRET, SYMBOL, TIMEFRAME, LIMIT, RISK_PERCENTAGE, TRADE_AMOUNT, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE
import ccxt

# Initialize exchange client (e.g., Binance)
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

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
