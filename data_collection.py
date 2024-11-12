# data_collection.py

import os
import pandas as pd
from forex_python.converter import CurrencyRates
from datetime import datetime, timedelta
import time

# Define a function to collect live data for a given currency pair
def get_live_data(base_currency="USD", target_currency="EUR"):
    cr = CurrencyRates()

    try:
        # Get the current exchange rate
        rate = cr.get_rate(base_currency, target_currency)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Live Data: {base_currency} to {target_currency} is {rate} at {timestamp}")
        return {
            'timestamp': timestamp,
            'base_currency': base_currency,
            'target_currency': target_currency,
            'rate': rate
        }
    except Exception as e:
        print(f"Error fetching live data: {e}")
        return None


# Define a function to collect historical data for a given currency pair
def get_historical_data(base_currency="USD", target_currency="EUR", start_date="2023-01-01", end_date="2023-12-31"):
    cr = CurrencyRates()

    try:
        # Convert string dates into datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Create a list to store the historical data
        historical_data = []

        # Loop through each day in the date range
        current_date = start_date
        while current_date <= end_date:
            rate = cr.get_rate(base_currency, target_currency, current_date)
            historical_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'base_currency': base_currency,
                'target_currency': target_currency,
                'rate': rate
            })
            current_date += timedelta(days=1)

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(historical_data)
        print(f"Historical Data collected from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        return df

    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None


# Save the data to CSV
def save_data_to_csv(data, file_name="forex_data.csv"):
    try:
        # Check if data is not empty and save it
        if data:
            df = pd.DataFrame(data)
            if not os.path.exists(file_name):
                df.to_csv(file_name, mode='w', index=False)
            else:
                df.to_csv(file_name, mode='a', header=False, index=False)
            print(f"Data saved to {file_name}")
        else:
            print("No data to save.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")


if __name__ == "__main__":
    # Collect and save live data (for example, USD to EUR every minute)
    live_data = get_live_data("USD", "EUR")
    if live_data:
        save_data_to_csv([live_data], "live_forex_data.csv")

    # Collect and save historical data (for example, USD to EUR from 2023-01-01 to 2023-12-31)
    historical_data = get_historical_data("USD", "EUR", "2023-01-01", "2023-12-31")
    if historical_data is not None:
        save_data_to_csv(historical_data, "historical_forex_data.csv")

    # Optionally, set this up to run periodically
    while True:
        # Collect live data every minute
        live_data = get_live_data("USD", "EUR")
        if live_data:
            save_data_to_csv([live_data], "live_forex_data.csv")
        
        # Sleep for 60 seconds before collecting data again
        time.sleep(60)
