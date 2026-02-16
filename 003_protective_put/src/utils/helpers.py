import pandas as pd
from datetime import datetime

class QuantUtils:
    @staticmethod
    def get_time_to_expiration(expiry_date: str) -> float:
        now = datetime.now()
        expiry = pd.to_datetime(expiry_date)
        days_remaining = (expiry - now).days
        return max(days_remaining / 365.25, 0.0001) 

    @staticmethod
    def clean_market_data(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [c.capitalize() for c in df.columns]
        return df.ffill().dropna()