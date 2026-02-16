import pandas as pd
import numpy as np
from src.core.engine import ProtectivePutEngine

def main():
    dates = pd.date_range(start="2024-01-01", periods=100)
    prices = 100 + np.cumsum(np.random.randn(100))
    df = pd.DataFrame({'Close': prices}, index=dates)

    print("--- Launching Quantitative Protective Put Strategy ---")

    engine = ProtectivePutEngine(df)

    results = engine.run_backtest()
    
    print("\nStrategy execution complete.")
    print(results[['Close', 'filtered_price', 'hedge_signal']].tail())

if __name__ == "__main__":
    main()