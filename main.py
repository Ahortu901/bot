import threading
import time
import asyncio
from model import load_trained_model, predict_next_price
from risk_management import RiskManagement
from api_utils import get_forex_price, place_buy_order, place_sell_order
from data_utils import load_forex_data

# Initialize Risk Management Model
account_balance = 1000  # Example account balance
risk_management = RiskManagement(account_balance)

# Load pre-trained GRU model for fast inference
model = load_trained_model('gru_forex_model.h5')  # Ensure you have your trained model file
filepath = 'forex_data.csv'  # Replace with your forex historical data file
data = load_forex_data(filepath)

# Global variables for shared state
current_price = None
predicted_price = None
pair = 'BTC_USDT'

# Fetch price function (run in a separate thread)
def fetch_price():
    global current_price
    while True:
        try:
            current_price = get_forex_price(pair)
            print(f"Fetched current price: {current_price}")
            time.sleep(5)  # Fetch every 5 seconds
        except Exception as e:
            print(f"Error fetching price: {e}")
            time.sleep(10)

# Prediction function (run in a separate thread)
def predict_price():
    global predicted_price
    while True:
        try:
            predicted_price = predict_next_price(model, data, lookback=60)
            print(f"Predicted next price: {predicted_price}")
            time.sleep(10)  # Predict every 10 seconds
        except Exception as e:
            print(f"Error predicting price: {e}")
            time.sleep(10)

# Trading and risk management function (run in a separate thread)
def trading_logic():
    while True:
        try:
            if current_price is not None and predicted_price is not None:
                price_difference = (predicted_price - current_price) / current_price
                print(f"Price Difference: {price_difference:.4f}")

                trade_amount = 0.001  # Example trade size
                buy_threshold = 0.02
                sell_threshold = 0.02

                # Buy decision
                if price_difference > buy_threshold:
                    print(f"Buy signal: {trade_amount} units of {pair}")
                    stop_loss_price = current_price * (1 - 0.02)  # 2% stop-loss
                    take_profit_price = current_price * (1 + 0.05)  # 5% take-profit
                    
                    if risk_management.execute_trade(current_price, stop_loss_price, take_profit_price):
                        place_buy_order(pair, trade_amount)

                # Sell decision
                elif price_difference < -sell_threshold:
                    print(f"Sell signal: {trade_amount} units of {pair}")
                    stop_loss_price = current_price * (1 + 0.02)  # 2% stop-loss
                    take_profit_price = current_price * (1 - 0.05)  # 5% take-profit

                    if risk_management.execute_trade(current_price, stop_loss_price, take_profit_price):
                        place_sell_order(pair, trade_amount)

            time.sleep(5)  # Check trading conditions every 5 seconds
        except Exception as e:
            print(f"Error in trading logic: {e}")
            time.sleep(10)

# Start all threads
def start_bot():
    fetch_thread = threading.Thread(target=fetch_price)
    predict_thread = threading.Thread(target=predict_price)
    trade_thread = threading.Thread(target=trading_logic)

    fetch_thread.start()
    predict_thread.start()
    trade_thread.start()

    fetch_thread.join()
    predict_thread.join()
    trade_thread.join()

# Run the bot
if __name__ == '__main__':
    start_bot()
