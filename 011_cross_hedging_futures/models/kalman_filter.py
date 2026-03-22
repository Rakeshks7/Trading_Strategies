import numpy as np
import pandas as pd
from typing import Tuple

class DynamicHedgeRatio:
    def __init__(self, trans_cov: float = 1e-4, obs_cov: float = 1e-2):
        self.trans_cov = trans_cov  
        self.obs_cov = obs_cov      
        
    def calculate_ohr(self, spot_returns: pd.Series, futures_returns: pd.Series) -> pd.Series:
        n = len(spot_returns)
        beta = np.zeros(n)
        p = np.zeros(n) 

        beta[0] = 0.0
        p[0] = 1.0

        y = spot_returns.values
        x = futures_returns.values
        
        for t in range(1, n):
            beta_prior = beta[t-1]
            p_prior = p[t-1] + self.trans_cov

            y_pred = beta_prior * x[t]
            error = y[t] - y_pred

            s = (x[t] ** 2) * p_prior + self.obs_cov

            k_gain = (p_prior * x[t]) / s

            beta[t] = beta_prior + k_gain * error
            p[t] = (1 - k_gain * x[t]) * p_prior
            
        return pd.Series(beta, index=spot_returns.index, name="Dynamic_OHR")