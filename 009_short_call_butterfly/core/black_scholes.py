import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Union

class BlackScholesEngine:
    
    def __init__(self, risk_free_rate: float = 0.04):
        self.r = risk_free_rate

    def d1(self, S: Union[float, pd.Series], K: Union[float, pd.Series], 
           T: Union[float, pd.Series], sigma: Union[float, pd.Series]) -> Union[float, pd.Series]:
        return (np.log(S / K) + (self.r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    def d2(self, d1_val: Union[float, pd.Series], T: Union[float, pd.Series], 
           sigma: Union[float, pd.Series]) -> Union[float, pd.Series]:
        return d1_val - sigma * np.sqrt(T)

    def call_price(self, S: pd.Series, K: pd.Series, T: pd.Series, sigma: pd.Series) -> pd.Series:
        d1_val = self.d1(S, K, T, sigma)
        d2_val = self.d2(d1_val, T, sigma)
        return (S * norm.cdf(d1_val) - K * np.exp(-self.r * T) * norm.cdf(d2_val))

    def call_delta(self, S: pd.Series, K: pd.Series, T: pd.Series, sigma: pd.Series) -> pd.Series:
        d1_val = self.d1(S, K, T, sigma)
        return norm.cdf(d1_val)
        
    def call_gamma(self, S: pd.Series, K: pd.Series, T: pd.Series, sigma: pd.Series) -> pd.Series:
        d1_val = self.d1(S, K, T, sigma)
        return norm.pdf(d1_val) / (S * sigma * np.sqrt(T))