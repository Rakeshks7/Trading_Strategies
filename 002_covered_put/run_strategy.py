from core.engine import CoveredPutEngine
from data.provider import MarketData
from core.margin_manager import MarginManager
import time

def run_strategy():
    print("--- Senior Quant Architect: Covered Put System ---")
    data_layer = MarketData()
    engine = CoveredPutEngine("TSLA")
    margin = MarginManager(initial_capital=1000000)
    
    while True:
        data = data_layer.get_data("TSLA")

        if margin.can_afford_short(data['spot'], 1000):
            target_delta = engine.select_strike(data['spot'], data['history'], [])
            
            if target_delta:
                print(f"Executing: Short 1000 TSLA, Sell {target_delta} Delta Put.")
            else:
                print("Risk check failed. Staying in cash.")
        
        time.sleep(3600) 

if __name__ == "__main__":
    run_strategy()