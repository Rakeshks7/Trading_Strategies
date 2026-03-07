import numpy as np

class RiskManager:
    def __init__(self, account_size: float, kelly_fraction: float, max_heat: float):
        self.account_size = account_size
        self.kelly_fraction = kelly_fraction
        self.max_heat = max_heat
        
    def calculate_position_size(self, win_prob: float, win_loss_ratio: float, max_loss_per_fly: float) -> int:
        if win_loss_ratio <= 0 or max_loss_per_fly <= 0:
            return 0

        kelly_pct = win_prob - ((1.0 - win_prob) / win_loss_ratio)

        if kelly_pct <= 0:
            return 0
            
        adj_kelly_pct = kelly_pct * self.kelly_fraction

        final_risk_pct = min(adj_kelly_pct, self.max_heat)
        
        capital_at_risk = self.account_size * final_risk_pct

        num_contracts = int(capital_at_risk / (max_loss_per_fly * 100))
        
        return num_contracts