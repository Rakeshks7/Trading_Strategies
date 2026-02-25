import pandas as pd
import numpy as np
from config import StrategyConfig

class PortfolioManager:
    def __init__(self, config: StrategyConfig):
        self.config = config

    def calculate_market_regime(self, benchmark: pd.Series) -> pd.Series:
        sma_200 = benchmark.rolling(window=self.config.regime_sma_days).mean()
        return (benchmark > sma_200).astype(int)

    def generate_target_weights(self, prices: pd.DataFrame, momentum_scores: pd.DataFrame, regime: pd.Series) -> pd.DataFrame:
        daily_returns = prices.pct_change()
        volatility = daily_returns.rolling(window=self.config.volatility_lookback).std()
        
        target_weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

        for date, scores in momentum_scores.iterrows():
            if regime.loc[date] == 0:
                continue

            valid_scores = scores.dropna()
            if valid_scores.empty:
                continue

            top_n = valid_scores.nlargest(self.config.top_n_assets).index

            inv_vol = 1.0 / volatility.loc[date, top_n]

            weights = inv_vol / inv_vol.sum()

            target_weights.loc[date, top_n] = weights
            
        return target_weights