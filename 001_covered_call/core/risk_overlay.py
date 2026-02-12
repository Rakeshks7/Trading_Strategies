import numpy as np

class RiskManager:
    def __init__(self, max_portfolio_heat: float = 0.20):
        self.max_heat = max_portfolio_heat

    def check_tail_risk(self, spot_price: float, iv: float) -> bool:
        return iv < 0.85 # Example threshold

    def apply_slippage(self, price: float, side: str) -> float:
        slippage = 0.0005 
        return price * (1 - slippage) if side == 'sell' else price * (1 + slippage)