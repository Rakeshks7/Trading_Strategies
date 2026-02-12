import pandas as pd
import numpy as np
from typing import Dict, Optional

class DataProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_latest_chain(self, ticker: str) -> pd.DataFrame:
        data = {
            'strike': [145, 150, 155, 160],
            'expiry': ['2026-03-20'] * 4,
            'type': ['call'] * 4,
            'bid': [7.2, 3.5, 1.1, 0.3],
            'ask': [7.5, 3.8, 1.3, 0.5],
            'iv': [0.22, 0.24, 0.28, 0.32],
            'delta': [0.75, 0.50, 0.25, 0.10]
        }
        return pd.DataFrame(data)

    def get_spot_price(self, ticker: str) -> float:
        return 152.45