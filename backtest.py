import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class Backtester:
    def __init__(self, data, model, risk_management, transaction_cost=0.001, slippage=0.0005, lookback=60):
        self.data = data
        self.model = model
        self.risk_management = risk_management
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.lookback = lookback

        self.initial_balance = 1000  # Example starting balance
        self.balance = self.initial_balance
        self.position = 0  # Current position (1 for long, -1 for short, 0 for no position)
        self.trade_history = []

    def apply_slippage(self, price):
        """Simulate slippage by introducing a small random offset."""
        return price * (1 + random.uniform(-self.slippage, self.slippage))

    def execute_trade(self, trade_type, price, trade_amount):
        """Execute trade considering transaction cost and slippage."""
        executed_price = self.apply_slippage(price)
        cost = trade_amount * executed_price * (1 + self.transaction_cost)

        if trade_type == 'buy' and self.balance >= cost:
            self.balance -= cost
            self.position = trade_amount
            self.trade_history.append(('buy', executed_price, trade_amount))

        elif trade_type == 'sell' and self.position >= trade_amount:
            self.balance += trade_amount * executed_price * (1 - self.transaction_cost)
            self.position -= trade_amount
            self.trade_history.append(('sell', executed_price, trade_amount))

    def backtest(self):
        """Run the backtest using vectorized operations."""
        results = []
        for i in range(self.lookback, len(self.data)):
            current_data = self.data.iloc[i - self.lookback:i]
            current_price = self.data.iloc[i]['Close']

            # Predict next price using model
            predicted_price = self.model.predict_next_price(current_data)

            # Calculate price difference
            price_difference = (predicted_price - current_price) / current_price

            # Define trade size
            trade_amount = 0.001  # Example trade size

            # Buy logic (threshold for buy signal)
            if price_difference > 0.02 and self.position == 0:  # Buy signal
                self.execute_trade('buy', current_price, trade_amount)

            # Sell logic (threshold for sell signal)
            elif price_difference < -0.02 and self.position > 0:  # Sell signal
                self.execute_trade('sell', current_price, trade_amount)

            # Track the balance at each step
            results.append({
                'date': self.data.iloc[i].name,
                'balance': self.balance + self.position * current_price,  # Account balance + open position value
                'position': self.position,
                'price': current_price,
                'predicted_price': predicted_price,
                'price_diff': price_difference
            })

        return pd.DataFrame(results)

    def walk_forward_testing(self, train_size=0.8):
        """Perform walk-forward testing by splitting the dataset into training and testing."""
        results = []

        # Split data into training and testing sets
        train_data, test_data = train_test_split(self.data, train_size=train_size, shuffle=False)
        
        # Walk-forward process
        for i in range(0, len(test_data), len(train_data)):
            train_split = test_data.iloc[i:i+len(train_data)]
            test_split = test_data.iloc[i+len(train_data):i+len(train_data)*2]

            # Re-train the model on each training split and test on the testing split
            self.model.train(train_split)
            
            # Backtest on the test split
            test_results = self.backtest(test_split)
            results.append(test_results)

        return results

    def plot_results(self, df):
        """Plot backtest results."""
        plt.figure(figsize=(10, 5))
        plt.plot(df['date'], df['balance'], label='Balance')
        plt.title('Backtest Results')
        plt.xlabel('Date')
        plt.ylabel('Balance')
        plt.legend()
        plt.show()

# Example model that can be replaced with your trained model
class ExampleModel:
    def predict_next_price(self, data):
        """Simple example model predicting next price based on moving average."""
        return data['Close'].mean()

    def train(self, data):
        """Dummy train method."""
        pass

# Example of backtest with random slippage and transaction costs
if __name__ == '__main__':
    # Load forex data
    data = pd.read_csv('forex_data.csv', parse_dates=['Date'], index_col='Date')

    # Initialize model and risk management
    model = ExampleModel()
    risk_management = None  # Replace with your risk management logic

    # Initialize backtester
    backtester = Backtester(data, model, risk_management, transaction_cost=0.001, slippage=0.0005)

    # Run backtest
    backtest_results = backtester.backtest()
    backtester.plot_results(backtest_results)

    # Perform Walk-Forward Testing
    walk_forward_results = backtester.walk_forward_testing(train_size=0.8)
    for result in walk_forward_results:
        backtester.plot_results(result)
