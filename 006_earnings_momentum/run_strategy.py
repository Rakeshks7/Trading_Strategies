import pandas as pd
import numpy as np
import logging
from core.data_engine import DataEngine
from alpha.signal_generator import SignalGenerator
from portfolio.risk_manager import RiskManager
from execution.backtest_simulator import BacktestSimulator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Earnings-Momentum Engine...")

    data_engine = DataEngine()
    signal_gen = SignalGenerator()
    risk_mgr = RiskManager(target_risk_per_trade=0.005) 
    simulator = BacktestSimulator(initial_capital=1000000.0, slippage_bps=10)

    logger.info("Loading price and fundamental data...")
    price_data, fundamentals = data_engine.fetch_mock_data()

    logger.info("Calculating SUE and Kalman-smoothed Momentum...")
    signals = signal_gen.generate_signals(price_data, fundamentals)

    logger.info("Applying ATR sizing and risk filters...")
    portfolio_targets = risk_mgr.size_positions(signals, price_data)

    logger.info("Running T+2 execution simulation...")
    results = simulator.run(portfolio_targets, price_data)
    
    logger.info(f"Simulation Complete. Final Portfolio Value: ${results['final_equity']:,.2f}")

if __name__ == "__main__":
    main()