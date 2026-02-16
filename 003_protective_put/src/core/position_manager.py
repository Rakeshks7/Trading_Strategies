from typing import Dict
import numpy as np
from src.analytics.greeks import OptionPricer

class PositionManager:
    def __init__(self, contract_size: int = 100):
        self.contract_size = contract_size

    def calculate_hedge_ratio(self, share_count: int, put_delta: float) -> int:
        contracts_needed = np.ceil(share_count / self.contract_size)
        return int(contracts_needed)

    def calculate_cost_basis_impact(self, stock_price: float, put_premium: float) -> float:
        return put_premium / stock_price