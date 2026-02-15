import numpy as np

class RegimeDetector:
    @staticmethod
    def calculate_hurst(price_series: np.ndarray) -> float:
        lags = range(2, 20)
        tau = [np.sqrt(np.std(np.subtract(price_series[lag:], price_series[:-lag]))) for lag in lags]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        return poly[0] * 2.0