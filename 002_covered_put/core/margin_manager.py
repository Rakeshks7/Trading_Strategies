class MarginManager:
    def __init__(self, initial_capital: float):
        self.capital = initial_capital
        self.maintenance_margin_rate = 0.30 

    def can_afford_short(self, spot_price: float, quantity: int) -> bool:
        required = spot_price * quantity * self.maintenance_margin_rate
        return self.capital > required