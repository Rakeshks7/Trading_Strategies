import numpy as np

class SqueezeProtector:
    def check_squeeze_risk(self, price_history: np.ndarray) -> bool:
        returns = np.diff(price_history) / price_history[:-1]
        z_score = (returns[-1] - np.mean(returns)) / np.std(returns)
        
        return z_score > 2.0  

    def model_slippage(self, volume: int, avg_volume: float) -> float:
        return 0.1 * (volume / avg_volume)**0.5