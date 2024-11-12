import pandas as pd
import logging
from forex_trading_strategy import load_data_with_indicators, generate_signals, backtest_strategy, plot_results
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
from trade import trade_forex

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# File to save the performance metrics
metrics_file = "performance_metrics.csv"

def load_data(file_path):
    try:
        df = load_data_with_indicators(file_path)
        logging.info(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def generate_signals_and_backtest(df):
    try:
        logging.info("Generating signals...")
        df = generate_signals(df)
        logging.info("Signals generated successfully.")
        
        logging.info("Backtesting the strategy...")
        df = backtest_strategy(df)
        logging.info("Backtest completed successfully.")
        return df
    except Exception as e:
        logging.error(f"Error during signal generation or backtesting: {e}")
        raise

def plot_and_print_results(df):
    try:
        logging.info("Plotting results...")
        plot_results(df)
        
        # Print final cumulative returns
        market_returns = df['Cumulative_returns'].iloc[-1]
        strategy_returns = df['Cumulative_strategy_returns'].iloc[-1]
        logging.info(f"Final Market Cumulative Returns: {market_returns:.2f}")
        logging.info(f"Final Strategy Cumulative Returns: {strategy_returns:.2f}")
        
        # Save performance metrics to a CSV file
        save_performance_metrics(market_returns, strategy_returns)
    except Exception as e:
        logging.error(f"Error while plotting results or printing final returns: {e}")
        raise

def save_performance_metrics(market_returns, strategy_returns):
    # Check if the metrics file exists, create it if not
    if not os.path.exists(metrics_file):
        metrics_df = pd.DataFrame(columns=["Market_Cumulative_Returns", "Strategy_Cumulative_Returns", "Timestamp"])
    else:
        metrics_df = pd.read_csv(metrics_file)

    # Add new performance data
    new_row = {
        "Market_Cumulative_Returns": market_returns,
        "Strategy_Cumulative_Returns": strategy_returns,
        "Timestamp": pd.Timestamp.now()
    }

    metrics_df = metrics_df.append(new_row, ignore_index=True)

    # Save to CSV
    metrics_df.to_csv(metrics_file, index=False)
    logging.info(f"Performance metrics saved to {metrics_file}")

def scheduled_job():
    # Assuming 'historical_forex_data_with_indicators.csv' exists in the same folder
    data_file = "historical_forex_data_with_indicators.csv"
    try:
        df = load_data(data_file)
        df = generate_signals_and_backtest(df)
        plot_and_print_results(df)
    except Exception as e:
        logging.error(f"Error during scheduled execution: {e}")

def schedule_task():
    # Set up the scheduler to run daily
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', days=1, next_run_time=pd.Timestamp.now())  # Daily execution
    scheduler.start()

    logging.info("Scheduler started. Press Ctrl+C to exit.")
    
    # Keep the script running so that the scheduler can keep working
    try:
        while True:
            time.sleep(60)  # Check every minute
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")

def main():
    # Automatically schedule the task when the script is run
    trade_forex()  # Replace with your actual trade function
    schedule_task()

if __name__ == "__main__":
    main()
