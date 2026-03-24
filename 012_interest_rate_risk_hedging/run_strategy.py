import pandas as pd
import numpy as np
import logging
from core.portfolio import BondPortfolio
from core.yield_curve import YieldCurveModel
from derivatives.futures import TreasuryFuture
from alpha.kalman_filter import DynamicBasisFilter
from risk.position_sizing import RiskManager

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_dummy_market_data() -> dict:
    return {
        "portfolio_yield": 4.25, 
        "ctd_yield": 4.10,       
        "portfolio_notional": 100_000_000, 
        "ctd_price": 98.50,
        "conversion_factor": 0.8543
    }

def main():
    logging.info("Initializing Structural Risk Transfer Pipeline...")

    market_data = fetch_dummy_market_data()

    portfolio = BondPortfolio(notional_value=market_data["portfolio_notional"])
    yc_model = YieldCurveModel()
    future = TreasuryFuture(symbol="ZN", ctd_price=market_data["ctd_price"], cf=market_data["conversion_factor"])

    kalman = DynamicBasisFilter(process_variance=1e-5, measurement_variance=1e-3)

    risk = RiskManager(max_margin_capital=5_000_000)

    try:

        port_dv01 = portfolio.calculate_dv01(modified_duration=7.5)
        logging.info(f"Portfolio DV01 (Cash Risk): ${port_dv01:,.2f} per bps")

        ctd_dv01 = future.calculate_ctd_dv01(modified_duration=6.8)
        logging.info(f"CTD DV01 (Derivative Risk): ${ctd_dv01:,.2f} per bps")

        raw_spread = market_data["portfolio_yield"] - market_data["ctd_yield"]
        filtered_spread = kalman.update(raw_spread)

        basis_adjustment_factor = 1.0 + (filtered_spread * 0.1) # Simplified scaling

        raw_contracts = (port_dv01 / ctd_dv01) * future.cf

        adjusted_contracts = raw_contracts * basis_adjustment_factor

        final_trade_qty = risk.apply_slippage_and_limits(
            target_contracts=adjusted_contracts, 
            current_position=0, # Assuming flat to start
            contract_multiplier=1000
        )
        
        logging.info(f"Raw Target Contracts: {raw_contracts:.2f}")
        logging.info(f"Kalman-Adjusted Contracts: {adjusted_contracts:.2f}")
        logging.info(f"RISK APPROVED EXECUTION: SHORT {final_trade_qty} {future.symbol} Contracts.")

    except Exception as e:
        logging.error(f"Critical Pipeline Failure: {str(e)}")

if __name__ == "__main__":
    main()