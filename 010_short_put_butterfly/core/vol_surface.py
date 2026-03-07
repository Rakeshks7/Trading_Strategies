import numpy as np

class VolatilitySurface:
    def __init__(self, atm_vol: float, skew_factor: float = 0.15):
        self.atm_vol = atm_vol
        self.skew_factor = skew_factor
        
    def get_iv(self, S: np.ndarray, K: np.ndarray) -> np.ndarray:
        moneyness = np.log(K / S)
        iv = self.atm_vol + (self.skew_factor * moneyness**2)
        return np.clip(iv, 0.05, 2.0) 