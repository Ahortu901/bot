import pandas as pd
import numpy as np

# Advanced strategy example
def advanced_strategy(prediction, df):
    # Example of a trend-following strategy: Moving Average Crossover
    short_window = 50
    long_window = 200

    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()

    # Signal based on moving averages
    if df['short_ma'].iloc[-1] > df['long_ma'].iloc[-1]:
        return 'buy', df['close'].iloc[-1]
    elif df['short_ma'].iloc[-1] < df['long_ma'].iloc[-1]:
        return 'sell', df['close'].iloc[-1]
    else:
        return None, None
