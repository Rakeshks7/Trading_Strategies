import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class OptionChainItem:
    strike: float
    expiration: str
    type: str  
    bid: float
    ask: float
    iv: float
    delta: float

class MarketDataHandler:
    
    def get_historical_prices(self, ticker: str, lookback: int) -> pd.DataFrame:
        dates = pd.date_range(end=pd.Timestamp.now(), periods=lookback)
        np.random.seed(42) 
        returns = np.random.normal(0.001, 0.02, lookback)
        price_path = 100 * np.cumprod(1 + returns)
        
        df = pd.DataFrame(data={'close': price_path}, index=dates)
        df['returns'] = df['close'].pct_change()
        return df

    def get_borrow_rate(self, ticker: str) -> float:
        if ticker.startswith('T'):
            return 0.15  
        return 0.01      

    def get_option_chain(self, ticker: str, spot_price: float) -> list[OptionChainItem]:
        chain = []
        strikes = np.linspace(spot_price * 0.9, spot_price * 1.1, 10)
        
        for k in strikes:
            moneyness = spot_price - k
            intrinsic = max(0, moneyness) # for calls this is usually spot - k, wait. 
            iv = 0.40 + (0.05 * (k/spot_price)) # Vol skew
            
            chain.append(OptionChainItem(
                strike=round(k, 2),
                expiration="2024-12-20",
                type='call',
                bid=round(max(0.1, (spot_price - k) + 2.0), 2), 
                ask=round(max(0.2, (spot_price - k) + 2.1), 2),
                iv=iv,
                delta=0.5 
            ))
        return chain