import numpy as np
from typing import Dict

class ButterflyEngine:
    def __init__(self, symbol: str, current_price: float, iv: float, dte: int):
        self.symbol = symbol
        self.S = current_price
        self.iv = iv
        self.dte = dte

    def _calculate_expected_move(self) -> float:
        return self.S * self.iv * np.sqrt(self.dte / 365.0)

    def calculate_strikes(self) -> Dict[str, float]:
        expected_move = self._calculate_expected_move()

        k2 = round(self.S) 
        k1 = round(self.S - expected_move)
        k3 = round(self.S + expected_move)

        wing_width = min(abs(k2 - k1), abs(k3 - k2))
        k1 = k2 - wing_width
        k3 = k2 + wing_width

        estimated_debit = wing_width * 0.15 
        
        return {
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "width": wing_width,
            "expected_move": expected_move,
            "max_loss": estimated_debit * 100 
        }