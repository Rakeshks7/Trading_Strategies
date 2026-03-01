import numpy as np
import pandas as pd
from typing import Dict, Tuple
from alpha.option_models import BlackScholesPricer
from data.market_data_handler import OptionChain

class DynamicStrikeOptimizer:
    def __init__(self, pricer: BlackScholesPricer):
        self.pricer = pricer

    def find_optimal_butterfly(self, chain: OptionChain) -> Dict[str, float]:
        S = chain.underlying_price

        idx_atm = np.argmin(np.abs(chain.strikes - S))
        k2 = chain.strikes[idx_atm]
        
        best_ev = -np.inf
        best_wings = (0.0, 0.0)

        for width in range(2, 11):
            k1 = k2 + width 
            k3 = k2 - width 

            if k1 not in chain.strikes or k3 not in chain.strikes:
                continue
                
            idx_k1 = np.where(chain.strikes == k1)[0][0]
            idx_k2 = np.where(chain.strikes == k2)[0][0]
            idx_k3 = np.where(chain.strikes == k3)[0][0]

            cost_k1 = chain.ask[idx_k1]
            credit_k2 = chain.bid[idx_k2] * 2
            cost_k3 = chain.ask[idx_k3]
            
            net_debit = cost_k1 - credit_k2 + cost_k3

            max_profit = width - net_debit
            if net_debit > 0 and max_profit > 0:
                reward_risk = max_profit / net_debit
                skew_penalty = chain.iv_surface[idx_k3] - chain.iv_surface[idx_k2]
                ev_score = reward_risk - (skew_penalty * 10)
                
                if ev_score > best_ev:
                    best_ev = ev_score
                    best_wings = (k1, k3)
                    
        return {
            "K1_ITM": best_wings[0],
            "K2_ATM": k2,
            "K3_OTM": best_wings[1],
            "Net_Debit": net_debit,
            "Max_Profit": best_wings[0] - k2 - net_debit
        }