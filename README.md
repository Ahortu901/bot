# Forex Trading Bot

A deep learning-based Forex trading bot that uses machine learning models to predict price trends, manage risks, and backtest strategies for real-time trading. The bot incorporates advanced risk management features, transaction costs, slippage simulation, and walk-forward testing for robust performance evaluation.

## Features

- **Deep Learning Model**: Predicts future price movements based on historical data.
- **Risk Management**: Ensures trades adhere to predefined risk parameters.
- **Backtesting**: Evaluate the bot's performance on historical data with realistic transaction costs and slippage.
- **Walk-Forward Testing**: Robust validation technique to avoid overfitting by retraining on different segments of data.
- **Multi-threaded Execution**: Designed for high-performance, real-time trading environments.

## Requirements

- Python 3.7+
- The following dependencies can be installed using `pip` from the provided `requirements.txt` file:

    ```txt
    numpy==1.24.0
    pandas==1.5.3
    matplotlib==3.7.0
    scikit-learn==1.2.0
    tensorflow==2.13.0
    keras==2.13.0
    requests==2.28.1
    aiohttp==3.8.1
    ```

## Installation

### Option 1: Using `requirements.txt`

1. Clone the repository or download the project files to your local machine.
2. Navigate to the project directory and create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Option 2: Using `setup.py`

1. Clone the repository or download the project files to your local machine.
2. Navigate to the project directory and install the dependencies using `setup.py`:

    ```bash
    python setup.py install
    ```

## Usage

### Backtesting

To run a backtest using historical Forex data, use the `backtest.py` script. Make sure to replace the `ExampleModel` class with your trained model.

1. Ensure you have historical Forex data in CSV format with at least the columns `Date` and `Close`. The `Date` column should be in a recognizable date format, and `Close` should represent the closing price of the Forex pair.
2. Run the backtest:

    ```bash
    python backtest.py
    ```

   This will print the backtest results and plot the balance over time.

### Live Trading (Simulation)

To run the bot for live trading, integrate your real-time data API (such as **Crypto.com** or other Forex API) into the model. Update the data-fetching logic in the `main.py` file and set up live trade execution through an API like **CCXT** or **Binance API**.

```python
# Example usage:
model = YourModel()  # Replace with your model
data = fetch_live_data()  # Your method for fetching live data
predicted_price = model.predict_next_price(data)
```

### Risk Management
The bot uses a risk management system to calculate position sizes and stop losses based on account equity. Make sure to configure the parameters in the risk_management.py file before using it.

### Walk-Forward Testing
The walk-forward testing method in backtest.py splits the dataset into training and testing sets. It retrains the model on different segments of the data and evaluates its performance. This helps in evaluating model performance over time and avoiding overfitting.

### Contributing
We welcome contributions! To contribute to the project:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them.
- Push the changes to your forked repository.
- Open a pull request with a clear description of your changes.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
- Thanks to the TensorFlow and Keras libraries for deep learning.
- Thanks to Pandas and NumPy for data processing and numerical computations.
- Special thanks to open-source contributors for making these libraries available.