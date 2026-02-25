import pandas as pd
import numpy as np
from config import StrategyConfig
from typing import Tuple



class AlphaGenerator:
    def __init__(self, config: StrategyConfig):
        self.config = config

    def _apply_kalman_filter(self, series: pd.Series) -> pd.Series:
        n = len(series)
        xhat = np.zeros(n) 
        P = np.zeros(n)    
        xhatminus = np.zeros(n) 
        Pminus = np.zeros(n)    
        K = np.zeros(n)    

        Q = self.config.kalman_process_variance
        R = self.config.kalman_measurement_variance

        xhat[0] = series.iloc[0]
        P[0] = 1.0
        
        prices = series.values
        
        for k in range(1, n):
            xhatminus[k] = xhat[k-1]
            Pminus[k] = P[k-1] + Q

            if np.isnan(prices[k]):
                xhat[k] = xhatminus[k]
                P[k] = Pminus[k]
                continue
                
            K[k] = Pminus[k] / (Pminus[k] + R)
            xhat[k] = xhatminus[k] + K[k] * (prices[k] - xhatminus[k])
            P[k] = (1 - K[k]) * Pminus[k]
            
        return pd.Series(xhat, index=series.index)

    def generate_signals(self, prices: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        print("Applying Kalman Filter to asset universe (this may take a moment)...")
        smoothed_prices = prices.apply(self._apply_kalman_filter)

        t_minus_1 = smoothed_prices.shift(self.config.momentum_skip_days)
        t_minus_12 = smoothed_prices.shift(self.config.momentum_lookback_days)

        momentum_scores = (t_minus_1 - t_minus_12) / t_minus_12
        
        return momentum_scores, smoothed_prices