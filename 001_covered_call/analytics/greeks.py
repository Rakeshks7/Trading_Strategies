import numpy as np
from scipy.stats import norm
from typing import Tuple

class OptionPricing:
    @staticmethod
    def calculate_greeks(S: np.ndarray, K: float, T: float, r: float, sigma: np.ndarray, option_type: str = 'call') -> dict:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            delta = norm.cdf(d1)
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
            vega = S * norm.pdf(d1) * np.sqrt(T)
            theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
        
        return {"delta": delta, "gamma": gamma, "vega": vega / 100, "theta": theta / 365}