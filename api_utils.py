import requests
import json
from config import API_KEY, API_SECRET

def get_crypto_data(symbol, timeframe, limit=1000):
    url = f"https://api.crypto.com/v2/public/get-candlestick"
    params = {
        "instrument_name": symbol,
        "timeframe": timeframe,
        "limit": limit
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}:{API_SECRET}"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['result']['data']
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def place_order(symbol, side, quantity, price, order_type="LIMIT"):
    url = f"https://api.crypto.com/v2/private/create-order"
    data = {
        "instrument_name": symbol,
        "side": side,
        "type": order_type,
        "price": price,
        "quantity": quantity
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}:{API_SECRET}"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()
