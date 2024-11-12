import requests
import ccxt
import pandas as pd

class DataCollector:
    def __init__(self, api_key, secret_key, symbol):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
        })
        self.symbol = symbol

    def fetch_crypto_price(self):
        """
        Fetch the current market price of the cryptocurrency.
        """
        ticker = self.exchange.fetch_ticker(self.symbol)
        return ticker['last']

    def fetch_blockchain_difficulty(self, blockchain='bitcoin'):
        """
        Fetch the current mining difficulty for the specified blockchain (default: Bitcoin).
        """
        url = f"https://api.blockchain.info/stats"
        data = requests.get(url).json()
        return data['difficulty']

    def fetch_mining_pool_stats(self, pool='ethash'):
        """
        Fetch mining pool statistics (example: Ethermine or other pools).
        """
        url = f"https://api.ethermine.org/miner/{pool}/stats"
        data = requests.get(url).json()
        return data['data']

    def fetch_energy_cost(self):
        """
        Fetch energy cost from a fixed source (example data for the energy price per kWh).
        """
        # Placeholder: You can integrate with real-time energy APIs.
        return 0.12  # Energy cost per kWh (example)

    def collect_data(self):
        """
        Collect all the necessary data for mining analysis.
        """
        price = self.fetch_crypto_price()
        difficulty = self.fetch_blockchain_difficulty()
        pool_stats = self.fetch_mining_pool_stats()
        energy_cost = self.fetch_energy_cost()

        # Prepare and return a DataFrame
        data = {
            "crypto_price": price,
            "mining_difficulty": difficulty,
            "hash_rate": pool_stats.get('hashrate', 0),
            "energy_cost": energy_cost,
            "power_usage": pool_stats.get('power_usage', 0)
        }

        df = pd.DataFrame([data])
        return df
