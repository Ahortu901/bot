# data_collection.py
import yfinance as yf
import pandas as pd
import logging

def collect_data(symbol='EURUSD=X', period='1mo', interval='1d'):
    """Collect Forex data using Yahoo Finance."""
    try:
        # Download Forex data
        df = yf.download(symbol, period=period, interval=interval)
        df.sort_index(ascending=True, inplace=True)
        logging.info(f"Data collected for {symbol} successfully.")
        return df
    except Exception as e:
        logging.error(f"Error collecting data: {e}")
        raise
