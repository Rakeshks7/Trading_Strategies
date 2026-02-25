import pandas as pd
import numpy as np
from config import StrategyConfig

class VectorizedBacktester:
    def __init__(self, config: StrategyConfig):
        self.config = config

    def run(self, prices: pd.DataFrame, target_weights: pd.DataFrame) -> pd.DataFrame:
        monthly_weights = target_weights.resample('BM').last()
        monthly_prices = prices.resample('BM').last()

        daily_weights = monthly_weights.reindex(prices.index).ffill().shift(1) 

        asset_returns = prices.pct_change()

        portfolio_gross_returns = (daily_weights * asset_returns).sum(axis=1)

        weight_changes = monthly_weights.diff().abs()
        monthly_turnover = weight_changes.sum(axis=1) 

        cost_per_trade = self.config.trading_fee_pct + (self.config.slippage_bps / 10000)
        transaction_costs = monthly_turnover * cost_per_trade

        transaction_costs = transaction_costs.reindex(prices.index).fillna(0)

        portfolio_net_returns = portfolio_gross_returns - transaction_costs

        equity_curve = (1 + portfolio_net_returns).cumprod()
        
        results = pd.DataFrame({
            'Gross Return': portfolio_gross_returns,
            'Net Return': portfolio_net_returns,
            'Equity Curve': equity_curve
        })
        
        return results