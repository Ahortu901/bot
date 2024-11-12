# utils/risk_management.py

def check_daily_loss(total_loss, max_loss):
    """ Check if the daily loss exceeds the maximum allowed loss. """
    if total_loss >= max_loss:
        return True
    return False

def calculate_position_size(balance, risk_percentage, stop_loss_pips):
    """ Calculate position size based on risk percentage and stop loss. """
    risk_amount = balance * risk_percentage / 100
    position_size = risk_amount / (stop_loss_pips * 10)  # 10 is for pip value
    return position_size
