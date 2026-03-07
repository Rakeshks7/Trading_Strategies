import numpy as np
from scipy.stats import norm

def calculate_d1_d2(S: np.ndarray, K: np.ndarray, T: float, r: float, sigma: np.ndarray) -> tuple:
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def put_price(S: np.ndarray, K: np.ndarray, T: float, r: float, sigma: np.ndarray) -> np.ndarray:
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def put_delta(S: np.ndarray, K: np.ndarray, T: float, r: float, sigma: np.ndarray) -> np.ndarray:
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    return norm.cdf(d1) - 1.0