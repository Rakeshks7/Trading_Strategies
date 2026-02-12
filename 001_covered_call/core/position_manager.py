class PositionManager:

    def __init__(self):
        self.active_position = False
        self.short_call_strike = None

    def should_roll(self, current_price: float, threshold: float = 1.02) -> bool:
        if self.short_call_strike and current_price >= (self.short_call_strike * threshold):
            return True
        return False

    def log_trade(self, details: dict):
        print(f"STAMPING TRADE: {details['action']} {details['strike']} @ {details['price']}")