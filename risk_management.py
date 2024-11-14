class RiskManagement:
    def __init__(self, account_balance, risk_percentage=0.02, max_drawdown=0.1):
        self.account_balance = account_balance
        self.risk_percentage = risk_percentage
        self.max_drawdown = max_drawdown
        self.max_loss = account_balance * max_drawdown
        self.balance_history = [account_balance]

    def calculate_position_size(self, entry_price, stop_loss_price):
        risk_per_trade = self.account_balance * self.risk_percentage
        risk_per_unit = abs(entry_price - stop_loss_price)
        position_size = risk_per_trade / risk_per_unit
        return position_size

    def calculate_stop_loss(self, entry_price, risk_to_reward_ratio, reward_percentage=0.05):
        reward_target = entry_price * (1 + reward_percentage)
        stop_loss_price = entry_price - (reward_target - entry_price) / risk_to_reward_ratio
        return stop_loss_price

    def check_max_drawdown(self):
        current_balance = self.account_balance
        self.balance_history.append(current_balance)
        peak_balance = max(self.balance_history)
        drawdown = (peak_balance - current_balance) / peak_balance
        if drawdown > self.max_drawdown:
            print(f"Warning: Drawdown exceeded! Current drawdown is {drawdown*100:.2f}%")
            return True
        return False

    def execute_trade(self, entry_price, stop_loss_price, take_profit_price):
        if self.check_max_drawdown():
            print("Trade cannot be executed due to drawdown limits.")
            return False
        
        position_size = self.calculate_position_size(entry_price, stop_loss_price)
        print(f"Calculated Position Size: {position_size:.2f} units")

        risk_to_reward_ratio = (take_profit_price - entry_price) / (entry_price - stop_loss_price)
        print(f"Risk-to-Reward Ratio: {risk_to_reward_ratio:.2f}")

        if risk_to_reward_ratio < 2:
            print(f"Trade skipped: Risk-to-Reward ratio of {risk_to_reward_ratio:.2f} is too low.")
            return False

        print(f"Executing trade: Buy {position_size:.2f} units at {entry_price:.2f}")
        # Integration with Crypto API to place the order:
        # e.g. place_buy_order(entry_price, position_size)
        
        return True
