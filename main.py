# main.py
import logging
import time
from trade import trade_forex
from config import INTERVAL

# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    """Main function to execute the trading bot."""
    logging.info("Starting the Forex Trading Bot...")

    try:
        # Run the trading function
        trade_forex()

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    while True:
        # Run the bot in an infinite loop with a delay between cycles
        main()

        logging.info(f"Waiting for the next execution cycle...")
        time.sleep(INTERVAL)  # Adjust the interval as necessary
