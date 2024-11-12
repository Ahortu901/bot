# config.py

# API keys for broker
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Trading settings
TRADING_PAIR = 'EUR/USD'
TIMEFRAME = '1h'  # 1h timeframe
POSITION_SIZE = 0.1  # Size of each trade in lots
STOP_LOSS_PIPS = 50  # Stop loss in pips
TAKE_PROFIT_PIPS = 100  # Take profit in pips

# Model parameters
MODEL_TYPE = 'LSTM'  # Could be LSTM, CNN, etc.
EPOCHS = 50
BATCH_SIZE = 32

# Risk management parameters
MAX_DAILY_LOSS = 100  # Max loss per day in USD
