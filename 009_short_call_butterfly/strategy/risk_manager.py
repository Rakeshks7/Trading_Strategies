import pandas as pd
import logging

class RiskManager:
    
    def __init__(self, account_size: float):
        self.account_size = account_size
        self.max_risk_per_trade = 0.02  
        self.logger = logging.getLogger("RiskManager")

    def model_slippage(self, bid: float, ask: float) -> float:
        spread = ask - bid
        mid = (bid + ask) / 2
        execution_price = mid + (spread * 0.1) 
        return execution_price

    def calculate_position_size(self, max_loss: float) -> int:
        capital_at_risk = self.account_size * self.max_risk_per_trade
        if max_loss <= 0:
            return 0
        
        num_contracts = int(capital_at_risk / max_loss)
        return max(1, num_contracts) 

    def validate_gamma_exposure(self, days_to_expiration: int) -> bool:
        if days_to_expiration < 5:
            self.logger.warning("REJECTED: DTE < 5. Gamma exposure exceeds threshold.")
            return False
        return True