import numpy as np
from scipy.stats import norm
from typing import Union, Tuple

class VectorizedBlackScholes:
    def __init__(self, risk_free_rate: float = 0.05):
        self.r = risk_free_rate

    def d1_d2(self, S: np.ndarray, K: np.ndarray, T: np.ndarray, sigma: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        T = np.maximum(T, 1e-5) 
        d1 = (np.log(S / K) + (self.r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2

    def price_call(self, S: np.ndarray, K: np.ndarray, T: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        d1, d2 = self.d1_d2(S, K, T, sigma)
        return S * norm.cdf(d1) - K * np.exp(-self.r * T) * norm.cdf(d2)

    def delta(self, S: np.ndarray, K: np.ndarray, T: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        d1, _ = self.d1_d2(S, K, T, sigma)
        return norm.cdf(d1)
        
    def theta(self, S: np.ndarray, K: np.ndarray, T: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        d1, d2 = self.d1_d2(S, K, T, sigma)
        term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        term2 = self.r * K * np.exp(-self.r * T) * norm.cdf(d2)
        return (term1 - term2) / 365.0 