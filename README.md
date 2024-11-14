# AI Trading Bot with Cryptocurrency Mining Model

This project implements an AI-powered trading bot integrated with a cryptocurrency mining profitability model. The bot predicts the profitability of mining operations based on real-time data such as cryptocurrency prices, blockchain mining difficulty, energy costs, and hardware specifications. The project also includes optimization techniques to improve mining hardware configurations.

## Features
- **Real-Time Data Integration**: Collects real-time data for cryptocurrency prices, blockchain difficulty, mining pool stats, and energy costs.
- **Mining Profitability Prediction**: Uses a machine learning model (Random Forest) to predict mining profitability based on mining difficulty, hash rate, energy cost, and crypto price.
- **Mining Hardware Optimization**: Optimizes hardware configuration for maximum mining profitability using optimization algorithms.
- **Trading Bot Integration**: The bot can make decisions based on mining profitability, deciding whether to continue mining operations or pause them.

## Requirements

### Python Libraries
To get started, you'll need the following Python libraries:
- `ccxt` - For cryptocurrency exchange data.
- `requests` - For fetching real-time mining pool data.
- `pandas` - For data handling and processing.
- `sklearn` - For machine learning (Random Forest for predicting mining profitability).
- `scipy` - For optimization algorithms to optimize hardware configuration.
- `joblib` - For saving and loading the trained machine learning model.
- `matplotlib` - For plotting feature importance.

You can install all the required dependencies by running:

```bash
pip install -r requirements.txt

```
## Setup
***API Keys Configuration:
Ensure you have API keys for the cryptocurrency exchange (e.g., Binance). Create a config.py file with your API keys as follows:
```python
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
SYMBOL = 'BTC/USDT'  # Change to your preferred trading pair

```
### Data Collection:

- The bot collects real-time data like cryptocurrency prices, blockchain difficulty, and energy costs from multiple sources like Binance and Ethermine APIs. Ensure your API keys are configured and ready to fetch live data.
Mining Data:

The DataCollector class fetches real-time mining-related data such as hash rates, mining difficulty, and energy costs.

### Mining Profitability Model:

- The MiningProfitabilityModel uses the Random Forest algorithm to predict mining profitability based on historical and real-time data.

### Hardware Optimization:

- The HardwareOptimization class uses optimization algorithms (e.g., scipy.optimize) to determine the optimal hardware configuration for mining operations.

## Usage
 Training the Mining Profitability Model: Before running the bot, you need to train the mining profitability model. You can do so by running the following code:
```bash
python mining_model.py
```
This will train the model based on historical mining data stored in a CSV file (`mining_data.csv`). Once the model is trained, it will be saved as `mining_profitability_model.pkl`.

Running the Mining Bot: To start the bot and begin mining operations based on real-time data and model predictions, run:
```bash
python bot.py
```
The bot will collect data every hour, predict mining profitability, and make decisions on whether to continue mining operations or pause them.

## Example Output
When the bot runs, you'll see output like this:
```bash
Predicted mining profitability: 0.0853
Mining operation is profitable! Start mining...
```
If the profitability prediction is above a certain threshold (e.g., 0.05), the bot will start mining. If it is lower, the bot will pause operations.

## Optimizing Hardware Configuration
The bot can also optimize mining hardware configuration to maximize profitability. Here's an example of the output from the hardware optimization process:
```bash
Optimized hardware configuration: Hash Rate: 600000, Power Usage: 1.2
```
This will optimize the hash rate and power usage of your mining hardware to achieve maximum profitability.

## Data Sources
- Binance API: Used for fetching real-time cryptocurrency price data.
- Blockchain.info: Provides blockchain mining difficulty data.
- Ethermine API: Fetches mining pool stats like hash rate and power usage.

## Contributions are Welcome!
We welcome contributions to improve and expand this project! If you'd like to contribute, please follow these steps:

- Fork the repository.
- Clone your forked repository to your local machine.
- Make your changes or add new features.
- Create a pull request with a description of your changes.

*** Guidelines:
- Please ensure that your code adheres to the existing code style.
- Provide clear comments and documentation where necessary.
- Write unit tests to cover your new features or bug fixes.
- By contributing to this project, you help make it better for the community. We appreciate your time and effort!

Thank you for considering contributing!

```
### Key Additions:
- **Contributions are Welcome**: This section encourages others to contribute to the project by forking the repository, making changes, and creating pull requests. It also includes guidelines to ensure contributions maintain the project's quality.

Feel free to adjust the guidelines based on your specific preferences for contributing!
```

fixing Ta-lib error
```
cd ta-lib
```
```
./configure --prefix=/usr 
```
```
make
```
or
```
sudo make install
```
```
pip install ta-lib
```