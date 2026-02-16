import numpy as np
from scipy.stats import norm

class OptionPricer:
    @staticmethod
    def calculate_delta(S: float, K: float, T: float, r: float, sigma: float) -> float:
        if T <= 0: return 0
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return norm.cdf(d1) - 1  # Put Delta

    @staticmethod
    def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)