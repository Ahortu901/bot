import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Forex data and technical indicators (assuming the technical indicators were calculated earlier)
def load_data_with_indicators(file_name="historical_forex_data_with_indicators.csv"):
    df = pd.read_csv(file_name)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# Define strategy rules
def generate_signals(df):
    # Initialize signals column
    df['Signal'] = 0  # 0 means no action (hold), 1 means buy, -1 means sell

    for i in range(1, len(df)):
        # Buy Condition (When model predicts price rise and technical indicators support buy)
        if df['rate'][i] > df['rate'][i-1] and df['RSI_14'][i] < 30 and df['MACD'][i] > df['MACD_signal'][i] and df['rate'][i] > df['SMA_14'][i]:
            df['Signal'][i] = 1  # Buy signal

        # Sell Condition (When model predicts price fall and technical indicators support sell)
        elif df['rate'][i] < df['rate'][i-1] and df['RSI_14'][i] > 70 and df['MACD'][i] < df['MACD_signal'][i] and df['rate'][i] < df['SMA_14'][i]:
            df['Signal'][i] = -1  # Sell signal

    return df

# Backtest the strategy
def backtest_strategy(df):
    df['Returns'] = df['rate'].pct_change()  # Daily returns

    # We want to calculate returns for the strategy based on the Signal
    df['Strategy_returns'] = df['Returns'] * df['Signal'].shift(1)  # Strategy takes action the next day

    # Calculate the cumulative returns for both the strategy and the market
    df['Cumulative_returns'] = (1 + df['Returns']).cumprod() - 1
    df['Cumulative_strategy_returns'] = (1 + df['Strategy_returns']).cumprod() - 1

    return df

# Plot the results
def plot_results(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Cumulative_returns'], label='Market Returns', color='blue')
    plt.plot(df['Cumulative_strategy_returns'], label='Strategy Returns', color='red')
    plt.title('Market vs Strategy Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()

# Execute the strategy
if __name__ == "__main__":
    # Load Forex data with technical indicators (replace with actual path to your data)
    df = load_data_with_indicators("historical_forex_data_with_indicators.csv")

    # Generate Buy/Sell/Hold signals based on the strategy rules
    df = generate_signals(df)

    # Backtest the strategy
    df = backtest_strategy(df)

    # Plot the results to compare market performance vs. strategy performance
    plot_results(df)

    # Display the final cumulative returns
    print(f"Final Market Cumulative Returns: {df['Cumulative_returns'].iloc[-1]:.2f}")
    print(f"Final Strategy Cumulative Returns: {df['Cumulative_strategy_returns'].iloc[-1]:.2f}")
