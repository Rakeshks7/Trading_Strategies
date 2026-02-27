import numpy as np
from scipy.interpolate import RectBivariateSpline
from typing import List, Tuple, Optional
import logging

class VolatilitySurface:
    def __init__(self):
        self.surface_interpolator = None
        self.dtes = None
        self.strikes = None
        self.iv_grid = None

    def fit_surface(self, dtes: np.ndarray, strikes: np.ndarray, iv_data: np.ndarray) -> bool:
        try:
            self.surface_interpolator = RectBivariateSpline(dtes, strikes, iv_data, kx=3, ky=3)
            
            self.dtes = dtes
            self.strikes = strikes
            self.iv_grid = iv_data
            
            logging.info("Volatility surface successfully calibrated.")
            return True
            
        except Exception as e:
            logging.error(f"Failed to fit volatility surface: {str(e)}")
            return False

    def get_iv(self, target_dte: float, target_strike: float) -> Optional[float]:
        if self.surface_interpolator is None:
            logging.warning("Cannot query IV: Surface has not been fitted.")
            return None

        interpolated_iv = self.surface_interpolator(target_dte, target_strike)[0, 0]
        return max(float(interpolated_iv), 0.01)

    def get_butterfly_ivs(self, target_dte: float, k1: float, k2: float, k3: float) -> Tuple[float, float, float]:
        iv_k1 = self.get_iv(target_dte, k1)
        iv_k2 = self.get_iv(target_dte, k2)
        iv_k3 = self.get_iv(target_dte, k3)
        
        return iv_k1, iv_k2, iv_k3