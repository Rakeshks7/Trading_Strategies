import pandas as pd
import numpy as np
import logging
from strategy.risk_manager import RiskManager
from core.vol_surface import VolatilityKalmanFilter

class ShortCallButterfly:
    
    def __init__(self, risk_manager: RiskManager):
        self.rm = risk_manager
        self.kf = VolatilityKalmanFilter()
        self.logger = logging.getLogger("StrategyLogic")

    def generate_signal(self, spot: float, ivr: float, chain: pd.DataFrame) -> dict:
        if ivr > 25:
            self.logger.info(f"Pass: IVR ({ivr}) is too high. Waiting for compression.")
            return {}

        chain = self.kf.smooth_chain_iv(chain)

        chain['distance'] = abs(chain['strike'] - spot)
        atm_row = chain.loc[chain['distance'].idxmin()]
        k2_strike = atm_row['strike']

        dte = atm_row['expiration_days']
        if not self.rm.validate_gamma_exposure(dte):
            return {}

        expected_move = spot * atm_row['iv_clean'] * np.sqrt(dte / 365.0)
        wing_width = round(expected_move / 5) * 5 
        
        if wing_width == 0:
            wing_width = 5 
            
        k1_strike = k2_strike - wing_width
        k3_strike = k2_strike + wing_width

        try:
            leg_k1 = chain[chain['strike'] == k1_strike].iloc[0]
            leg_k2 = atm_row
            leg_k3 = chain[chain['strike'] == k3_strike].iloc[0]
        except IndexError:
            self.logger.error("Failed to find corresponding strikes for wings.")
            return {}

        credit_k1 = self.rm.model_slippage(leg_k1['bid'], leg_k1['ask']) 
        debit_k2 = self.rm.model_slippage(leg_k2['bid'], leg_k2['ask'])  
        credit_k3 = self.rm.model_slippage(leg_k3['bid'], leg_k3['ask']) 
        
        net_credit = credit_k1 - (2 * debit_k2) + credit_k3
        max_loss = wing_width - net_credit

        if net_credit <= (wing_width * 0.15):
            self.logger.warning(f"Pass: Net credit {net_credit:.2f} too low for width {wing_width}.")
            return {}

        contracts = self.rm.calculate_position_size(max_loss * 100) 

        return {
            "strategy": "Short Call Butterfly",
            "k1_short": k1_strike,
            "k2_long": k2_strike,
            "k3_short": k3_strike,
            "net_credit": net_credit,
            "max_loss": max_loss,
            "contracts": contracts,
            "expected_move_calculated": expected_move
        }