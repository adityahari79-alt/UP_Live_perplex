class PositionManager:
    def __init__(self, entry_price, profit_pct=10, stop_loss_pct=1, trailing_pct=1):
        self.entry_price = entry_price
        self.profit_target = entry_price * (1 + profit_pct / 100)
        self.stop_loss = entry_price * (1 - stop_loss_pct / 100)
        self.trailing_pct = trailing_pct
        self.highest_price = entry_price  # Track highest since entry

    def update(self, last_price):
        # Update trailing stop logic
        if last_price > self.highest_price:
            self.highest_price = last_price
            self.stop_loss = self.highest_price * (1 - self.trailing_pct / 100)

        # Check for exit signals
        if last_price >= self.profit_target:
            return "TAKE_PROFIT"
        elif last_price <= self.stop_loss:
            return "STOP_LOSS"
        return None