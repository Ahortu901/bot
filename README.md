# AI Trading Bot for Forex and Cryptocurrency

This project implements an advanced AI trading bot for Forex and cryptocurrency markets using deep learning. The bot predicts future price movements based on historical market data, executes trades, and manages risk using machine learning models. It integrates with the Crypto.com API for live trading and allows for backtesting and paper trading.

## Features

- **Deep Learning Model**: Predicts future price movements based on historical data using an LSTM neural network.
- **Risk Management**: Calculates position size based on portfolio balance and stop-loss limits.
- **Live Trading**: Trades live on the market using the Crypto.com API.
- **Backtesting**: Simulates trading using historical data to evaluate performance.
- **Paper Trading**: Executes trades in real-time but without risking real capital.

## Requirements

### Python 3.6+ and Dependencies

This project requires Python 3.6 or higher. To install the required dependencies, you can either use `requirements.txt` or `setup.py`.

### Required Libraries

- TensorFlow (for deep learning)
- NumPy, Pandas (for data manipulation)
- Matplotlib (for plotting)
- Requests (for interacting with Crypto.com API)
- scikit-learn (for data preprocessing and validation)
- TA-Lib (for technical analysis)

### Installation

#### Option 1: Using `setup.py`

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AITradingBot.git
   cd AITradingBot

## Install the dependencies:
```bash
python setup.py install
```
### Clone the repository:
```bash
git clone https://github.com/yourusername/AITradingBot.git
cd AITradingBot
```

### Create a Virtual Environment (Optional but Recommended)
It's recommended to use a virtual environment to avoid dependency conflicts.

- Create a virtual environment:
```bash
python3 -m venv venv
```

### Activate the virtual environment:

- For Linux/Mac:
```bash
source venv/bin/activate
```
### For Windows:
```bash
venv\Scripts\activate
```
Install dependencies as described above.

### Configuration
Before running the bot, configure the necessary settings:

** config.py
- API Keys: You will need to obtain API keys from Crypto.com to interact with their API.
```python
API_KEY = 'your_crypto_com_api_key'
API_SECRET = 'your_crypto_com_api_secret'
```
- Risk Management Settings: Set the maximum percentage of your portfolio to risk per trade, as well as the maximum position size.

```python
MAX_RISK_PERCENTAGE = 0.02  # Max risk per trade (2%)
MAX_POSITION_SIZE = 0.1     # Max position size (10% of portfolio)
```

- Model Configuration: Adjust model training settings like window size, batch size, and epochs.
```python
WINDOW_SIZE = 60   # Look-back window for predicting
BATCH_SIZE = 32    # Batch size for training
EPOCHS = 50        # Number of epochs for training
```

- Historical Data Configuration: Choose data source and timeframe for trading.
```python
DATA_SOURCE = "crypto_com"  # Data source for market data
TIMEFRAME = "1h"           # Timeframe for trading (1-hour candlesticks)
```

### Running the Bot
Live Trading (Paper Trading Mode)
To simulate real-time trading (without risking actual capital), you can use the Paper Trading mode. This mode fetches real-time data and simulates trades in the market.

- Run the bot:
```bash
python main.py
```
Choose ``live``for paper trading when prompted.

- Backtesting
To test your AI trading strategy on historical data and evaluate performance, you can run a backtest.

** Run the bot:
```bash
python main.py
```

Choose backtest for backtesting when prompted.

The backtest will simulate trades based on historical market data and show the final portfolio balance and performance.

Training the Model
The bot uses an LSTM (Long Short-Term Memory) model to predict future price movements based on historical data.

 1. The model will automatically train if no pre-trained model exists.
 2. You can also train the model manually by calling the train_model function in the trained_model.py file.

### Model Training Workflow

 1. Fetch historical market data.
 2. Preprocess the data (normalize and create windows of data for training).
 3. Train the model on the preprocessed data using LSTM.
 4. Save the trained model to a file for future use.


### Predicting Future Prices
Once the model is trained, it will be used to predict future prices based on the latest market data. The model uses the last WINDOW_SIZE hours (or other configured time frames) to make predictions.

 ### older Structure

```graphql
├── AITradingBot/
│   ├── main.py               # Main script to run the bot
│   ├── trained_model.py      # Contains model training logic
│   ├── model.py              # Model architecture (LSTM)
│   ├── risk_management.py    # Risk management logic (position sizing)
│   ├── api_utils.py          # API integration with Crypto.com
│   ├── config.py             # Configuration file
│   ├── setup.py              # Package setup script
│   ├── data_utils.py         # Data preprocessing functions
│   └── backtest.py           # Backtesting logic
├── requirements.txt          # List of required Python packages
└── README.md                 # Project documentation
```

### Backtesting Results

After running backtests, the bot will generate a DataFrame with trade actions and portfolio balances over time. You can analyze the backtest results to evaluate the performance of the trading strategy.

### Example Output of Backtest:

```yaml
Backtest completed.
   timestamp        action   price   quantity   portfolio_balance
0  2024-11-14 12:00:00   BUY       10000    0.10         9990
1  2024-11-14 13:00:00   SELL      10200    0.10         10195
2  2024-11-14 14:00:00   BUY       10150    0.10         10150
...
```

### Contributing

Feel free to fork the repository and submit pull requests for improvements, bug fixes, or new features. Please ensure that your contributions follow the coding standards and include relevant tests.

### License
This project is licensed under the MIT License - see the LICENSE file for details.