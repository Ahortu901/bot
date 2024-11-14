import time
import hmac
import hashlib
import requests

# Configure your API keys
#API_KEY = 'your_api_key'
#SECRET_KEY = 'your_secret_key'


import configparser

# Create a config parser object
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

# Access API keys and configuration values
API_KEY = config['API_KEYS']['CRYPTO_API_KEY']
SECRET_KEY = config['API_KEYS']['CRYPTO_API_SECRET']
BASE_URL = 'https://api.crypto.com/v2/'

# Access other parameters
transaction_cost = float(config['CONFIG']['TRANSACTION_COST'])
slippage = float(config['CONFIG']['SLIPPAGE'])
max_risk_per_trade = float(config['CONFIG']['MAX_RISK_PER_TRADE'])
stop_loss_percentage = float(config['CONFIG']['STOP_LOSS_PERCENTAGE'])
take_profit_percentage = float(config['CONFIG']['TAKE_PROFIT_PERCENTAGE'])


# Helper functions for request signing
def create_signature(params, secret_key):
    param_string = "".join([f"{k}{v}" for k, v in sorted(params.items())])
    return hmac.new(bytes(secret_key, 'utf-8'), param_string.encode('utf-8'), hashlib.sha256).hexdigest()

def send_signed_request(endpoint, params=None):
    params = params or {}
    params['api_key'] = API_KEY
    params['id'] = int(time.time() * 1000)
    params['sig'] = create_signature(params, SECRET_KEY)
    response = requests.post(BASE_URL + endpoint, json=params)
    return response.json()

# Fetch current forex price
def get_forex_price(pair):
    endpoint = 'public/get-ticker'
    response = requests.get(BASE_URL + endpoint, params={'instrument_name': pair})
    data = response.json()
    return float(data['result']['data'][0]['a'])  # Ask price

# Place a buy order
def place_buy_order(pair, amount):
    endpoint = 'private/create-order'
    params = {
        'instrument_name': pair,
        'side': 'BUY',
        'type': 'LIMIT',
        'price': get_forex_price(pair), 
        'quantity': amount
    }
    response = send_signed_request(endpoint, params)
    return response

# Place a sell order
def place_sell_order(pair, amount):
    endpoint = 'private/create-order'
    params = {
        'instrument_name': pair,
        'side': 'SELL',
        'type': 'LIMIT',
        'price': get_forex_price(pair), 
        'quantity': amount
    }
    response = send_signed_request(endpoint, params)
    return response
