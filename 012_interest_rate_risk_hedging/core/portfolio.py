import numpy as np

class BondPortfolio:
    def __init__(self, notional_value: float):
        self.notional = notional_value

    def calculate_dv01(self, modified_duration: float) -> float:
        """
        Calculates the Dollar Value of a 1 Basis Point move (DV01).
        
        Math: DV01 = Notional * Modified Duration * 0.0001
        
        Args:
            modified_duration (float): The weighted average mod duration of the portfolio.
        Returns:
            float: Dollar value change for a 1 bps rate shock.
        """
        bps_shift = 0.0001
        return self.notional * modified_duration * bps_shift