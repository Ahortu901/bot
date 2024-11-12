import logging
import numpy as np
import pandas as pd

def sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate the annualized Sharpe ratio with a risk-free rate.

    Parameters:
    - returns (pandas.Series): Strategy returns (daily or other time intervals).
    - risk_free_rate (float): Risk-free rate as a decimal (e.g., 0.02 for 2%).

    Returns:
    - float: The annualized Sharpe ratio.
    """
    try:
        # Subtract the risk-free rate from returns to get excess returns
        excess_returns = returns - risk_free_rate

        # Annualize the Sharpe ratio assuming 252 trading days per year
        annualized_sharpe = np.sqrt(252) * (excess_returns.mean() / excess_returns.std()) # type: ignore

        return annualized_sharpe
    except Exception as e:
        logging.error(f"Error calculating Sharpe ratio: {e}")
        raise
