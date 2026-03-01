import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class OptionChain:
    strikes: np.ndarray
    iv_surface: np.ndarray
    bid: np.ndarray
    ask: np.ndarray
    underlying_price: float
    dte: float

class MarketDataHandler:
    def __init__(self, ticker: str):
        self.ticker = ticker
        
    def fetch_current_chain(self) -> OptionChain:
        spot = 100.0
        strikes = np.linspace(80, 120, 41)

        base_iv = 0.20
        iv_surface = base_iv + 0.0005 * (strikes - spot)**2 - 0.002 * (strikes - spot)

        spreads = 0.05 + 0.005 * np.abs(strikes - spot)
        mid_prices = np.maximum(0.5, 10 * iv_surface - 0.1 * np.abs(strikes - spot))
        
        bids = mid_prices - (spreads / 2)
        asks = mid_prices + (spreads / 2)
        
        return OptionChain(
            strikes=strikes,
            iv_surface=iv_surface,
            bid=bids,
            ask=asks,
            underlying_price=spot,
            dte=45 / 365.0
        )