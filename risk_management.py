from config import MAX_RISK_PERCENTAGE, MAX_POSITION_SIZE

def calculate_risk(portfolio_balance, trade_price, trade_quantity):
    risk = portfolio_balance * MAX_RISK_PERCENTAGE
    return risk

def calculate_position_size(portfolio_balance, current_price, stop_loss_price):
    risk = calculate_risk(portfolio_balance, current_price, stop_loss_price)
    position_size = risk / abs(current_price - stop_loss_price)
    position_size = min(position_size, portfolio_balance * MAX_POSITION_SIZE)
    return position_size
