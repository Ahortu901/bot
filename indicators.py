# utils/indicators.py

import talib

def rsi(data, period=14):
    """ Calculate the Relative Strength Index (RSI). """
    return talib.RSI(data['Close'], timeperiod=period)

def macd(data):
    """ Calculate the MACD (Moving Average Convergence Divergence). """
    macd, macdsignal, macdhist = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, macdsignal
