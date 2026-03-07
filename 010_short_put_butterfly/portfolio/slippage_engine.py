import numpy as np

class SlippageModel:
    def __init__(self, base_spread: float = 0.02, itm_penalty_factor: float = 0.10):
        self.base_spread = base_spread
        self.itm_penalty_factor = itm_penalty_factor
        
    def estimate_slippage(self, S: np.ndarray, K: np.ndarray) -> np.ndarray:
        moneyness = K / S
        itm_extent = np.maximum(0, moneyness - 1.0)
        
        spread = self.base_spread + (itm_extent * self.itm_penalty_factor)
        slippage_cost = spread / 2.0 
        return slippage_cost