import ccxt
import pandas as pd

# Fetch historical data
def fetch_data(exchange, symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Save data to CSV for training
def save_data(df, file_path):
    df.to_csv(file_path, index=False)
