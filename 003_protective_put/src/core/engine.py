import pandas as pd
import numpy as np
from src.analytics.filters.py import SignalProcessor
from src.analytics.greeks import OptionPricer

class ProtectivePutEngine:
    def __init__(self, data: pd.DataFrame, initial_cap: float = 100000):
        self.data = data
        self.equity = initial_cap
        self.positions = []

    def run_backtest(self):
        self.data['filtered_price'] = SignalProcessor.apply_kalman_filter(self.data['Close'].values)

        self.data['hedge_signal'] = np.where(self.data['filtered_price'] > self.data['Close'], 1, 0)

        print("Backtest processed with Kalman Signal.")
        return self.data