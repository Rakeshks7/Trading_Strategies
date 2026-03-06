import pandas as pd
import numpy as np
from typing import Tuple

class DataLoader:
    
    def __init__(self, ticker: str):
        self.ticker = ticker

    def fetch_live_chain(self, current_price: float) -> pd.DataFrame:
        strikes = np.arange(current_price - 20, current_price + 25, 5)
        
        data = []
        for K in strikes:
            base_iv = 0.20
            skew = 0.001 * (current_price - K)
            iv = base_iv + skew + np.random.normal(0, 0.005) 
            
            spread = 0.05 + 0.01 * abs(current_price - K)
            theoretical_price = max(0.1, 5.0 - 0.2 * abs(current_price - K))
            
            data.append({
                'strike': K,
                'type': 'call',
                'expiration_days': 30,
                'bid': theoretical_price - (spread / 2),
                'ask': theoretical_price + (spread / 2),
                'iv_noisy': iv
            })
            
        return pd.DataFrame(data)
    
    def get_underlying_metrics(self) -> Tuple[float, float]:
        spot_price = 150.00
        ivr = 18.5  
        return spot_price, ivr