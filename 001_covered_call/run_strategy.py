import sys
import time
from core.engine import CoveredCallEngine

def run_strategy():
    print("--- Initializing Production Covered Call Engine ---")
    strategy = CoveredCallEngine(ticker="AAPL")

    try:
        while True:
            # In production: spot, iv = data_provider.get_latest()
            sim_spot = 150.0
            sim_iv = 0.25
            
            signal = strategy.generate_signal(sim_spot, sim_iv, [])
            
            if signal:
                print(f"Signal Generated: {signal['action']} at Delta {signal['target_delta']}")
            
            time.sleep(60) # Poll every minute
    except KeyboardInterrupt:
        print("Shutting down gracefully...")

if __name__ == "__main__":
    run_strategy()