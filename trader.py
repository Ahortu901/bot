import ccxt
import logging

# Function to execute trades
def execute_trade(exchange, action, symbol, amount):
    try:
        balance = exchange.fetch_balance()
        usdt_balance = balance['total']['USDT']
        btc_balance = balance['total']['BTC']

        if action == 'buy' and usdt_balance > 10:
            exchange.create_market_buy_order(symbol, amount)
            print(f"Executed Buy Order: {amount} {symbol}")
        elif action == 'sell' and btc_balance > 0.001:
            exchange.create_market_sell_order(symbol, amount)
            print(f"Executed Sell Order: {amount} {symbol}")
    except Exception as e:
        logging.error(f"Error executing trade: {e}")

# Get account balance
def get_balance(exchange):
    balance = exchange.fetch_balance()
    return balance['total']
