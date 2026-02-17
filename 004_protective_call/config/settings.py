from dataclasses import dataclass

@dataclass
class StrategyConfig:
    TICKERS = ["TSLA", "NVDA", "AMD"]  
    BENCHMARK_TICKER = "SPY"

    MAX_CAPITAL_ALLOCATION = 0.20      
    MAX_THETA_BILL = 0.05             
    HARD_STOP_LOSS_PCT = 0.15         
    TARGET_PROFIT_PCT = 0.30

    LOOKBACK_PERIOD = 252             
    Z_SCORE_ENTRY = 2.0               

    TARGET_DELTA = 0.30               
    DAYS_TO_EXPIRATION = 45           
    MAX_IMPLIED_VOL_PERCENTILE = 80   

config = StrategyConfig()