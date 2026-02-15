import pandas as pd

class MarketData:
    def get_data(self, ticker: str):
        return {
            "spot": 100.0,
            "history": np.random.normal(100, 2, 100),
            "borrow_rate": 0.02 # 2% per annum to borrow the stock
        }