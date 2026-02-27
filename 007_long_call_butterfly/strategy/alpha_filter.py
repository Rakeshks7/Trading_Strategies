import numpy as np
from typing import List

class KalmanVolatilityFilter:
    def __init__(self, process_variance: float = 1e-4, measurement_variance: float = 1e-2):
        self.Q = process_variance     
        self.R = measurement_variance 
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def filter_volatility(self, noisy_iv_series: List[float]) -> np.ndarray:
        
        filtered_states = []

        if noisy_iv_series:
            self.posteri_estimate = noisy_iv_series[0]
            
        for measurement in noisy_iv_series:
            priori_estimate = self.posteri_estimate
            priori_error_estimate = self.posteri_error_estimate + self.Q

            blending_factor = priori_error_estimate / (priori_error_estimate + self.R)
            self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
            self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
            
            filtered_states.append(self.posteri_estimate)
            
        return np.array(filtered_states)