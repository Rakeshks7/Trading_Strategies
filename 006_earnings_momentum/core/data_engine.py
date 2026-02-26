import pandas as pd
import numpy as np
from typing import Tuple

class DataEngine:
    
    def __init__(self):
        pass

    def fetch_mock_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        dates = pd.date_range(start="2024-01-01", periods=252, freq="B")
        tickers = ["AAPL", "MSFT", "NVDA"]

        price_records = []
        for ticker in tickers:
            prices = np.cumprod(1 + np.random.normal(0.0005, 0.015, len(dates))) * 100
            highs = prices * (1 + np.random.uniform(0.001, 0.01, len(dates)))
            lows = prices * (1 - np.random.uniform(0.001, 0.01, len(dates)))
            df = pd.DataFrame({'date': dates, 'ticker': ticker, 'close': prices, 'high': highs, 'low': lows})
            price_records.append(df)
            
        price_data = pd.concat(price_records).set_index(['date', 'ticker'])

        fundamentals = pd.DataFrame({
            'date': [pd.to_datetime("2024-04-15")] * 3,
            'ticker': tickers,
            'eps_actual': [1.50, 2.10, 0.95],
            'eps_forecast': [1.45, 1.90, 0.90],
            'eps_std_dev': [0.02, 0.05, 0.01]
        }).set_index(['date', 'ticker'])
        
        return price_data, fundamentals