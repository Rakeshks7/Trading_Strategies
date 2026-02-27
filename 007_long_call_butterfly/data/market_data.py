import numpy as np
from typing import List

class MarketDataFeed:
    def get_historical_iv(self, symbol: str, lookback_days: int = 30) -> List[float]:
        base_iv = np.linspace(0.40, 0.50, lookback_days) 
        noise = np.random.normal(0, 0.05, lookback_days)
        
        noisy_iv = base_iv + noise
        return noisy_iv.tolist()