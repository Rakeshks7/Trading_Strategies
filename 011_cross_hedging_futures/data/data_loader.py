import yfinance as yf
import pandas as pd
import numpy as np
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class DataLoader:
    def __init__(self, spot_ticker: str, futures_ticker: str):
        self.spot_ticker = spot_ticker
        self.futures_ticker = futures_ticker

    def fetch_data(self, start_date: str, end_date: str) -> Tuple[pd.Series, pd.Series]:
        logging.info(f"Fetching data for {self.spot_ticker} and {self.futures_ticker}...")
        try:
            data = yf.download([self.spot_ticker, self.futures_ticker], start=start_date, end=end_date)['Adj Close']
            
            data = data.dropna()
            
            spot_prices = data[self.spot_ticker]
            futures_prices = data[self.futures_ticker]
            
            logging.info(f"Successfully loaded {len(data)} aligned price points.")
            return spot_prices, futures_prices
            
        except Exception as e:
            logging.error(f"Failed to fetch data: {e}")
            raise