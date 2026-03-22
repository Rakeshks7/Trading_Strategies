import pandas as pd
import numpy as np
import logging

class PositionManager:
    def __init__(self, spot_position_value: float, futures_multiplier: float):
        self.spot_value = spot_position_value
        self.multiplier = futures_multiplier

    def calculate_contracts(self, dynamic_ohr: pd.Series, futures_prices: pd.Series) -> pd.Series:
        logging.info("Calculating required futures contracts for dynamic hedging...")

        futures_notional = futures_prices * self.multiplier

        raw_contracts = dynamic_ohr * (self.spot_value / futures_notional)

        actual_contracts = np.round(raw_contracts)
        
        return actual_contracts