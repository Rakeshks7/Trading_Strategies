from dataclasses import dataclass

@dataclass
class StrategyConfig:
    momentum_lookback_days: int = 252  
    momentum_skip_days: int = 21       
    regime_sma_days: int = 200         
    volatility_lookback: int = 63      

    top_n_assets: int = 20             

    slippage_bps: float = 5.0          
    trading_fee_pct: float = 0.001     

    kalman_process_variance: float = 1e-5
    kalman_measurement_variance: float = 1e-3