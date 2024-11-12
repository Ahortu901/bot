# config.py

# Configuration settings for the bot
API_KEY = 'your_api_key_here'  # If using a broker API
SECRET_KEY = 'your_secret_key_here'  # If using a broker API

# Settings for data collection and trading
TRADING_PAIR = 'EURUSD=X'  # Forex pair
INTERVAL = 60  # Time interval in seconds between each trade execution cycle
DATA_PERIOD = '1y'  # Data collection period (can be '1mo', '1d', etc.)
DATA_INTERVAL = '1h'  # Data collection interval (e.g., '1d', '1h', '5m')

# Model configuration
MODEL_PATH = "model/deep_learning_model.h5"  # Path to the saved model