import pandas as pd
import numpy as np
import logging

class RiskManager:
    def __init__(self, zscore_threshold: float = 3.0, window: int = 60):
        self.threshold = zscore_threshold
        self.window = window

    def track_basis_risk(self, spot_returns: pd.Series, futures_returns: pd.Series, dynamic_ohr: pd.Series) -> pd.Series:
        logging.info("Running tail-risk basis analysis...")

        basis_returns = spot_returns - (dynamic_ohr * futures_returns)

        rolling_mean = basis_returns.rolling(window=self.window).mean()
        rolling_std = basis_returns.rolling(window=self.window).std()
        
        z_scores = (basis_returns - rolling_mean) / rolling_std

        black_swan_flags = np.abs(z_scores) > self.threshold
        
        if black_swan_flags.any():
            breaches = black_swan_flags.sum()
            logging.warning(f"⚠️ DANGER: {breaches} basis deviations exceeded Z-Score {self.threshold}. Structural decoupling detected.")
            
        return z_scores