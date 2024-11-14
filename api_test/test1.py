import hashlib
import hmac
import time
import requests

# Your Crypto.com API and Secret keys
API_KEY = 'xKEj9UeUerUTncjpR6cZ7R'
SECRET_KEY = 'cxakp_h2A3FuM39bihJ5ezgroWvB'

# Crypto.com API endpoint
BASE_URL = 'https://api.crypto.com/v2'

def generate_signature(params, secret_key):
    """Generate HMAC SHA256 signature required by Crypto.com API."""
    params_str = ''.join(f"{key}{params[key]}" for key in sorted(params))
    return hmac.new(
        bytes(secret_key, 'utf-8'),
        bytes(params_str, 'utf-8'),
        hashlib.sha256
    ).hexdigest()

def get_account_balance():
    """Fetch account balance from Crypto.com."""
    path = '/private/get-account-summary'
    params = {
        'id': 1,  # Unique identifier for your request
        'method': 'private/get-account-summary',
        'api_key': API_KEY,
        'nonce': int(time.time() * 1000)  # A unique nonce based on timestamp
    }

    # Generate signature
    params['sig'] = generate_signature(params, SECRET_KEY)

    # Make the request
    response = requests.post(BASE_URL + path, json=params)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Fetch and display the account balance
account_balance = get_account_balance()
print(account_balance)
