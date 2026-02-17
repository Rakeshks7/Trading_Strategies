import math
from config.settings import config

class RiskManager:
    
    def calculate_position_size(self, account_value: float, entry_price: float, volatility: float) -> int:
        risk_amount = account_value * 0.02

        estimated_max_loss_per_share = entry_price * 0.10 
        
        shares = math.floor(risk_amount / estimated_max_loss_per_share)
        return shares

    def validate_trade(self, borrow_rate: float, iv_percentile: float) -> bool:
        if borrow_rate > 0.10: 
            print(f"RISK REJECT: Borrow rate {borrow_rate:.1%} is too high.")
            return False

        if iv_percentile > config.MAX_IMPLIED_VOL_PERCENTILE:
            print(f"RISK REJECT: IV Percentile {iv_percentile} too high. Options expensive.")
            return False
            
        return True