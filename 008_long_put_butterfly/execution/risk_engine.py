import numpy as np

class RiskEngine:
    def __init__(self, max_slippage: float = 0.05):
        self.max_slippage = max_slippage

    def validate_execution_quality(self, net_debit: float, mid_price: float) -> bool:
        slippage = abs(net_debit - mid_price)
        slippage_pct = slippage / mid_price if mid_price > 0 else 1.0
        
        if slippage_pct > self.max_slippage:
            return False
        return True

    def calculate_gamma_risk(self, S: float, K2: float, days_to_expiry: int) -> str:
        if days_to_expiry < 7 and abs(S - K2) < 2.0:
            return "CRITICAL: High Gamma Pin Risk. Recommend Exit."
        return "SAFE"