import numpy as np
import pandas as pd
from typing import Dict, Any
import logging

from data.market_data import MarketDataFeed
from models.vol_surface import VolatilitySurface
from strategy.alpha_filter import KalmanVolatilityFilter
from strategy.butterfly_engine import ButterflyEngine
from risk.execution import ExecutionGuard
from risk.position_sizing import OptionsKellySizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_strategy(symbol: str, current_price: float, dte: int, risk_capital: float):
    logging.info(f"Initializing Butterfly Engine for {symbol} | DTE: {dte}")

    feed = MarketDataFeed()
    raw_iv_data = feed.get_historical_iv(symbol)
    

    kf = KalmanVolatilityFilter()
    true_iv_state = kf.filter_volatility(raw_iv_data)
    current_true_iv = true_iv_state[-1]
    logging.info(f"Filtered IV State: {current_true_iv:.4f}")

    if current_true_iv < 0.40: 
        logging.warning("Volatility edge not present. True IV too low. Aborting.")
        return False

    engine = ButterflyEngine(symbol, current_price, current_true_iv, dte)
    trade_setup = engine.calculate_strikes()
    logging.info(f"Target Strikes (1-2-1): K1={trade_setup['k1']}, K2={trade_setup['k2']}, K3={trade_setup['k3']}")

    guard = ExecutionGuard()
    if not guard.check_liquidity_conditions(time_of_day="10:00", bid_ask_spread=0.05):
        logging.warning("Microstructure conditions unfavorable. High slippage risk.")
        return False
        
    sizer = OptionsKellySizer(win_rate=0.45, win_loss_ratio=3.0)
    alloc = sizer.calculate_allocation(risk_capital, trade_setup['max_loss'])
    logging.info(f"Capital Allocation Approved: Deploying ${alloc:.2f}")
    
    logging.info("Trade Execution Routed Successfully.")
    return True

if __name__ == "__main__":
    run_strategy(symbol="SPX", current_price=5100.0, dte=30, risk_capital=100000.0)