import numpy as np
from scipy.stats import norm
from typing import Tuple

class BlackScholesPricer:
    def __init__(self, risk_free_rate: float = 0.045):
        self.r = risk_free_rate

    def put_price_and_greeks(
        self, S: float, K: np.ndarray, T: float, sigma: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        T = np.maximum(T, 1e-5) 
        
        d1 = (np.log(S / K) + (self.r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        price = K * np.exp(-self.r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        delta = norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        
        theta_term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        theta_term2 = self.r * K * np.exp(-self.r * T) * norm.cdf(-d2)
        theta = (theta_term1 + theta_term2) / 365.0 # Daily theta
        
        return price, delta, gamma, theta