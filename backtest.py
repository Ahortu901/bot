import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import mean_squared_error
from calculate_sharpe_ratio import sharpe_ratio
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def load_data_with_indicators(file_path):
    """Load Forex data with technical indicators."""
    try:
        df = pd.read_csv(file_path, parse_dates=True, index_col="Date")
        logging.info(f"Data loaded from {file_path}.")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def generate_signals(df):
    """Generate trading signals based on technical indicators."""
    try:
        df['Signal'] = 0
        # Example: A simple moving average strategy (SMA)
        short_window = 40
        long_window = 100

        df['Short_SMA'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        df['Long_SMA'] = df['Close'].rolling(window=long_window, min_periods=1).mean()

        df['Signal'][short_window:] = np.where(df['Short_SMA'][short_window:] > df['Long_SMA'][short_window:], 1, 0)  # Buy Signal
        df['Signal'][short_window:] = np.where(df['Short_SMA'][short_window:] < df['Long_SMA'][short_window:], -1, 0)  # Sell Signal

        df['Position'] = df['Signal'].diff()  # Detect the change in signal (entry/exit points)

        logging.info("Signals generated based on SMAs.")
        return df
    except Exception as e:
        logging.error(f"Error generating signals: {e}")
        raise

def backtest_strategy(df):
    """Backtest the trading strategy and calculate performance metrics."""
    try:
        df['Daily_Return'] = df['Close'].pct_change()
        df['Strategy_Return'] = df['Daily_Return'] * df['Position'].shift(1)  # Calculate strategy return

        # Calculate cumulative returns
        df['Cumulative_Market_Returns'] = (1 + df['Daily_Return']).cumprod() - 1
        df['Cumulative_Strategy_Returns'] = (1 + df['Strategy_Return']).cumprod() - 1

        # Performance metrics
        cumulative_market_return = df['Cumulative_Market_Returns'].iloc[-1]
        cumulative_strategy_return = df['Cumulative_Strategy_Returns'].iloc[-1]
        annualized_sharpe_ratio = calculate_sharpe_ratio(df['Strategy_Return'])
        max_drawdown = calculate_max_drawdown(df['Cumulative_Strategy_Returns'])

        logging.info(f"Cumulative Market Return: {cumulative_market_return:.2f}")
        logging.info(f"Cumulative Strategy Return: {cumulative_strategy_return:.2f}")
        logging.info(f"Annualized Sharpe Ratio: {annualized_sharpe_ratio:.2f}")
        logging.info(f"Max Drawdown: {max_drawdown:.2f}")

        return df, cumulative_market_return, cumulative_strategy_return, annualized_sharpe_ratio, max_drawdown
    except Exception as e:
        logging.error(f"Error in backtesting strategy: {e}")
        raise

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """Calculate the annualized Sharpe ratio."""
    try:
        excess_returns = returns - risk_free_rate
        annualized_sharpe = np.sqrt(252) * (excess_returns.mean() / excess_returns.std())  # Assuming 252 trading days
        return annualized_sharpe
    except Exception as e:
        logging.error(f"Error calculating Sharpe ratio: {e}")
        raise

def calculate_max_drawdown(cumulative_returns):
    """Calculate the maximum drawdown."""
    try:
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        return max_drawdown
    except Exception as e:
        logging.error(f"Error calculating max drawdown: {e}")
        raise

def plot_results(df):
    """Plot the results of the strategy and market."""
    try:
        plt.figure(figsize=(14, 7))
        plt.plot(df['Cumulative_Market_Returns'], label='Market Cumulative Returns', color='blue')
        plt.plot(df['Cumulative_Strategy_Returns'], label='Strategy Cumulative Returns', color='orange')
        plt.title('Market vs. Strategy Cumulative Returns')
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.grid(True)
        plt.show()
        logging.info("Results plotted successfully.")
    except Exception as e:
        logging.error(f"Error plotting results: {e}")
        raise

def backtest_and_evaluate(file_path):
    """Run backtest and evaluate performance."""
    try:
        # Load data with indicators
        df = load_data_with_indicators(file_path)

        # Generate signals based on technical indicators
        df = generate_signals(df)

        # Backtest strategy and calculate performance
        df, cumulative_market_return, cumulative_strategy_return, sharpe_ratio, max_drawdown = backtest_strategy(df)

        # Plot results
        plot_results(df)

        # Return performance metrics
        performance_metrics = {
            'Cumulative Market Return': cumulative_market_return,
            'Cumulative Strategy Return': cumulative_strategy_return,
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown
        }
        
        logging.info(f"Performance metrics: {performance_metrics}")
        return performance_metrics

    except Exception as e:
        logging.error(f"Error in backtesting and evaluation: {e}")
        raise

if __name__ == "__main__":
    # Example usage with a CSV file containing Forex data and indicators
    file_path = 'historical_forex_data_with_indicators.csv'  # Replace with your actual file path
    performance_metrics = backtest_and_evaluate(file_path)
    print("Performance metrics:", performance_metrics)
