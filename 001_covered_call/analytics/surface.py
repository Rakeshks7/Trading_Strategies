import numpy as np
from scipy.interpolate import CubicSpline

class VolatilitySurface:
    @staticmethod
    def calculate_skew(strikes: np.ndarray, ivs: np.ndarray) -> float:
        if len(strikes) < 3:
            return 0.0

        slope, _ = np.polyfit(strikes, ivs, 1)
        return slope

    def get_interpolated_iv(self, target_strike: float, strikes: np.ndarray, ivs: np.ndarray) -> float:
        spline = CubicSpline(strikes, ivs)
        return float(spline(target_strike))