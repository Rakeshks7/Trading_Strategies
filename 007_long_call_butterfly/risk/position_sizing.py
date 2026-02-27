class OptionsKellySizer:
    def __init__(self, win_rate: float, win_loss_ratio: float, kelly_fraction: float = 0.5):
        self.W = win_rate
        self.R = win_loss_ratio
        self.fraction = kelly_fraction 

    def calculate_allocation(self, total_capital: float, max_loss_per_trade: float) -> float:
        kelly_percentage = self.W - ((1.0 - self.W) / self.R)
        
        if kelly_percentage <= 0:
            return 0.0 
            
        target_risk_capital = total_capital * (kelly_percentage * self.fraction)

        number_of_contracts = max(1, int(target_risk_capital // max_loss_per_trade))
        
        return number_of_contracts * max_loss_per_trade