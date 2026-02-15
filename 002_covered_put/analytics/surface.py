import numpy as np

class PutSkewAnalyzer:
    @staticmethod
    def get_skew_premium(atm_iv: float, otm_iv: float) -> float:
        return otm_iv - atm_iv 