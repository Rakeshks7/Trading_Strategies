from analytics.hurst_exponent import RegimeDetector
from analytics.greeks import PutGreeks
from core.risk_overlay import SqueezeProtector

class CoveredPutEngine:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.regime_tool = RegimeDetector()
        self.risk = SqueezeProtector()

    def select_strike(self, spot: float, price_history: np.ndarray, put_chain: list):
        h = self.regime_tool.calculate_hurst(price_history)

        target_delta = -0.15 if h > 0.5 else -0.35
        
        if self.risk.check_squeeze_risk(price_history):
            return None 
            
        return target_delta