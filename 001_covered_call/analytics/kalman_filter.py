import numpy as np

class SignalSmoother:
    def __init__(self, process_variance: float = 1e-5, measurement_variance: float = 1e-3):
        self.post_estimate = 0.0
        self.post_error_estimate = 1.0
        self.Q = process_variance
        self.R = measurement_variance

    def update(self, measurement: float) -> float:
        pri_estimate = self.post_estimate
        pri_error_estimate = self.post_error_estimate + self.Q

        blending_factor = pri_error_estimate / (pri_error_estimate + self.R)
        self.post_estimate = pri_estimate + blending_factor * (measurement - pri_estimate)
        self.post_error_estimate = (1 - blending_factor) * pri_error_estimate
        
        return self.post_estimate