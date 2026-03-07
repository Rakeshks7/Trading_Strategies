import numpy as np
import pandas as pd

class VolatilitySqueezeDetector:
    def __init__(self, lookback: int, threshold: float):
        self.lookback = lookback
        self.threshold = threshold
        
    def generate_signal(self, close_prices: pd.Series) -> bool:
        if len(close_prices) < self.lookback:
            return False
            
        rolling_mean = close_prices.rolling(window=20).mean()
        rolling_std = close_prices.rolling(window=20).std()
        
        upper_band = rolling_mean + (rolling_std * 2)
        lower_band = rolling_mean - (rolling_std * 2)
        
        bb_width = (upper_band - lower_band) / rolling_mean

        current_width = bb_width.iloc[-1]
        historical_widths = bb_width.dropna().tail(self.lookback)
        
        if len(historical_widths) == 0:
            return False
            
        percentile = (historical_widths < current_width).mean()

        return percentile < self.threshold