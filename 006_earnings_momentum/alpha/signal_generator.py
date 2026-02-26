import pandas as pd
import numpy as np
from typing import Optional

class SignalGenerator:
    
    def __init__(self, momentum_window: int = 126, skip_window: int = 21):
        self.momentum_window = momentum_window
        self.skip_window = skip_window

    def calculate_sue(self, fundamentals: pd.DataFrame) -> pd.Series:
        std_dev = np.where(fundamentals['eps_std_dev'] == 0, 1e-6, fundamentals['eps_std_dev'])
        sue = (fundamentals['eps_actual'] - fundamentals['eps_forecast']) / std_dev
        return sue

    def apply_kalman_filter(self, prices: pd.Series) -> pd.Series:
        n_iter = len(prices)
        sz = (n_iter,) 
        
        Q = 1e-5 
        R = 0.01 
        
        xhat = np.zeros(sz)      
        P = np.zeros(sz)         
        xhatminus = np.zeros(sz) 
        Pminus = np.zeros(sz)    
        K = np.zeros(sz)         

        xhat[0] = prices.iloc[0]
        P[0] = 1.0
        
        for k in range(1, n_iter):
            xhatminus[k] = xhat[k-1]
            Pminus[k] = P[k-1] + Q

            K[k] = Pminus[k] / ( Pminus[k] + R )
            xhat[k] = xhatminus[k] + K[k] * (prices.iloc[k] - xhatminus[k])
            P[k] = (1 - K[k]) * Pminus[k]
            
        return pd.Series(xhat, index=prices.index)

    def generate_signals(self, price_data: pd.DataFrame, fundamentals: pd.DataFrame) -> pd.DataFrame:
        sue = self.calculate_sue(fundamentals)

        signals = pd.DataFrame(index=fundamentals.index)
        signals['SUE'] = sue
        signals['Trade_Signal'] = signals['SUE'] > 1.5 
        
        return signals[signals['Trade_Signal'] == True]