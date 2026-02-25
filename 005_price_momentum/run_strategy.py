import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import StrategyConfig
from data.loader import DataLoader
from signals.alpha_generator import AlphaGenerator
from risk.portfolio_manager import PortfolioManager
from execution.backtester import VectorizedBacktester

def generate_dummy_data(days=1000, assets=50):
    np.random.seed(42)
    dates = pd.date_range(start="2015-01-01", periods=days, freq='B')
    returns = np.random.normal(0.0005, 0.02, (days, assets))
    prices = np.exp(np.cumsum(returns, axis=0)) * 100
    df = pd.DataFrame(prices, index=dates, columns=[f"TICKER_{i}" for i in range(assets)])

    spy_returns = np.random.normal(0.0004, 0.012, days)
    spy_prices = np.exp(np.cumsum(spy_returns)) * 200
    df['SPY'] = spy_prices
    
    df.to_csv("dummy_market_data.csv")
    print("Generated dummy_market_data.csv")

def main():
    print("--- Initializing Price Momentum Strategy ---")

    generate_dummy_data()

    config = StrategyConfig()

    loader = DataLoader("dummy_market_data.csv")
    prices, benchmark = loader.load_and_clean()

    alpha = AlphaGenerator(config)
    momentum_scores, smoothed_prices = alpha.generate_signals(prices)

    risk_manager = PortfolioManager(config)
    regime = risk_manager.calculate_market_regime(benchmark)
    target_weights = risk_manager.generate_target_weights(prices, momentum_scores, regime)

    engine = VectorizedBacktester(config)
    results = engine.run(prices, target_weights)

    total_return = (results['Equity Curve'].iloc[-1] - 1) * 100
    print(f"\n--- Backtest Complete ---")
    print(f"Total Net Return: {total_return:.2f}%")

    results['Equity Curve'].plot(title="Kalman-Smoothed Momentum Equity Curve", figsize=(10,5))
    plt.ylabel("Cumulative Return")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()