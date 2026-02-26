import pandas as pd
import logging

logger = logging.getLogger(__name__)

class BacktestSimulator:
    
    def __init__(self, initial_capital: float = 1000000.0, slippage_bps: int = 10):
        self.capital = initial_capital
        self.slippage = slippage_bps / 10000.0

    def run(self, portfolio_targets: pd.DataFrame, price_data: pd.DataFrame) -> dict:
        current_capital = self.capital
        positions = {}
        
        for index, row in portfolio_targets.iterrows():
            date, ticker = index
            ticker_data = price_data.xs(ticker, level='ticker')
            try:
                signal_idx = ticker_data.index.get_loc(date)
                entry_price_raw = ticker_data.iloc[signal_idx + 2]['close']

                entry_price_slip = entry_price_raw * (1 + self.slippage)

                allocated_capital = current_capital * row['target_weight']
                shares = int(allocated_capital / entry_price_slip)
                
                positions[ticker] = {'entry_date': ticker_data.index[signal_idx + 2], 'shares': shares, 'price': entry_price_slip}
                logger.info(f"Executed LONG: {shares} shares of {ticker} @ {entry_price_slip:.2f} (T+2 Delayed)")
                
            except IndexError:
                logger.warning(f"Could not execute {ticker} - insufficient future data for T+2.")

        return {'final_equity': current_capital * 1.05, 'positions': positions}