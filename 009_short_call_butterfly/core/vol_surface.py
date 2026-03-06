import numpy as np
import pandas as pd

class VolatilityKalmanFilter:
    
    def __init__(self, process_variance: float = 1e-5, measurement_variance: float = 1e-3):
        self.posteri_estimate = 0.20 
        self.posteri_error_estimate = 1.0

        self.Q = process_variance 
        self.R = measurement_variance 

    def update(self, measurement: float) -> float:
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.Q

        blending_factor = priori_error_estimate / (priori_error_estimate + self.R)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

        return self.posteri_estimate

    def smooth_chain_iv(self, chain: pd.DataFrame) -> pd.DataFrame:
        smoothed_ivs = []
        for iv in chain['iv_noisy']:
            smoothed_ivs.append(self.update(iv))
        
        chain['iv_clean'] = smoothed_ivs
        return chain