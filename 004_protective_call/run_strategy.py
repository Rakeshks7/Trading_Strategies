from strategy.protective_call import ProtectiveCallStrategy
from config.settings import config

def main():
    print("Initializing Quantitative Engine...")
    print(f"Strategy: Protective Call | Universe: {config.TICKERS}")
    print("-------------------------------------------------------")
    
    account_value = 100000.00 
    
    for ticker in config.TICKERS:
        strategy = ProtectiveCallStrategy(ticker, account_value)
        strategy.run_analysis()

if __name__ == "__main__":
    main()