import pandas as pd
import numpy as np

class RiskManager:
    
    def __init__(self, target_risk_per_trade: float = 0.005, max_portfolio_heat: float = 0.20):
        self.target_risk = target_risk_per_trade
        self.max_heat = max_portfolio_heat

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(window=period).mean()

    def size_positions(self, signals: pd.DataFrame, price_data: pd.DataFrame, capital: float = 1000000.0) -> pd.DataFrame:
        targets = signals.copy()
        targets['target_weight'] = 0.05 
        return targets