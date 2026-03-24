import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

class YieldCurveModel:
    def __init__(self):
        self.curve_data = pd.DataFrame()

    def interpolate_yield(self, target_maturity: float, market_nodes: dict) -> float:
        maturities = np.array(list(market_nodes.keys()))
        yields = np.array(list(market_nodes.values()))

        sort_idx = np.argsort(maturities)
        cs = CubicSpline(maturities[sort_idx], yields[sort_idx])
        
        return float(cs(target_maturity))