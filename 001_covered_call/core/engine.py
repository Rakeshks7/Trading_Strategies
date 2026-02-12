from analytics.kalman_filter import SignalSmoother
from analytics.greeks import OptionPricing
from core.risk_overlay import RiskManager

class CoveredCallEngine:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.kf = SignalSmoother()
        self.risk = RiskManager()
        
    def generate_signal(self, current_price: float, iv: float, chain_data: list):
        filtered_price = self.kf.update(current_price)

        target_delta = 0.20 if current_price > filtered_price else 0.35

        if not self.risk.check_tail_risk(current_price, iv):
            return None # Market too volatile
            
        return {"action": "SELL_CALL", "target_delta": target_delta}