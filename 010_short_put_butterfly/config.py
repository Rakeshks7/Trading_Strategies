from dataclasses import dataclass

@dataclass
class StrategyConfig:
    risk_free_rate: float = 0.045

    target_dte: float = 45.0 / 365.0  
    wing_width_std: float = 1.0       

    lookback_window: int = 126        
    squeeze_percentile_threshold: float = 0.10 

    account_size: float = 1_000_000.0
    kelly_fraction: float = 0.25      
    max_portfolio_heat: float = 0.02  