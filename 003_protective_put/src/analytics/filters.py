import numpy as np
from pykalman import KalmanFilter

class SignalProcessor:
    @staticmethod
    def apply_kalman_filter(series: np.ndarray):
        kf = KalmanFilter(transition_matrices=[1],
                          observation_matrices=[1],
                          initial_state_mean=series[0],
                          initial_state_covariance=1,
                          observation_covariance=1,
                          transition_covariance=0.01)
        
        state_means, _ = kf.filter(series)
        return state_means.flatten()