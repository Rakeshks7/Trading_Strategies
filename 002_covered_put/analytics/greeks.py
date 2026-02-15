import numpy as np
from scipy.stats import norm

class PutGreeks:
    @staticmethod
    def get_put_stats(S: float, K: float, T: float, r: float, sigma: float):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        delta = norm.cdf(d1) - 1
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        
        return {"delta": delta, "theta": theta / 365, "vegas": (S * norm.pdf(d1) * np.sqrt(T)) / 100}