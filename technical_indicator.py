import pandas as pd
import talib
import numpy as np

# Load the historical Forex data
def load_data(file_name="historical_forex_data.csv"):
    df = pd.read_csv(file_name)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# Add technical indicators
def add_technical_indicators(df):
    # Moving Averages
    df['SMA_14'] = talib.SMA(df['rate'], timeperiod=14)  # 14-period Simple Moving Average
    df['EMA_14'] = talib.EMA(df['rate'], timeperiod=14)  # 14-period Exponential Moving Average

    # Relative Strength Index (RSI)
    df['RSI_14'] = talib.RSI(df['rate'], timeperiod=14)  # 14-period RSI

    # Moving Average Convergence Divergence (MACD)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['rate'], fastperiod=12, slowperiod=26, signalperiod=9)

    # Bollinger Bands (BB)
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(df['rate'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    # Stochastic Oscillator
    df['STOCH_slowk'], df['STOCH_slowd'] = talib.STOCH(df['rate'], df['rate'], df['rate'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    # On-Balance Volume (OBV)
    df['OBV'] = talib.OBV(df['rate'], df['volume'])  # Assuming there is a 'volume' column in the data

    # Average True Range (ATR)
    df['ATR'] = talib.ATR(df['high'], df['low'], df['rate'], timeperiod=14)

    # Parabolic SAR
    df['SAR'] = talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)

    return df

# Example Usage
if __name__ == "__main__":
    # Load data (replace with your actual data path)
    df = load_data("historical_forex_data.csv")

    # Add technical indicators
    df_with_indicators = add_technical_indicators(df)

    # Display first few rows to inspect
    print(df_with_indicators.head())
