import pandas as pd
import numpy as np
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_and_clean(self) -> Tuple[pd.DataFrame, pd.Series]:
        logger.info(f"Loading data from {self.file_path}...")
        try:
            df = pd.read_csv(self.file_path, index_col=0, parse_dates=True)

            df = df.ffill().dropna(axis=1, thresh=252)

            if 'SPY' not in df.columns:
                raise ValueError("Benchmark ticker 'SPY' must be in the dataset for regime filtering.")
            
            benchmark = df['SPY']
            prices = df.drop(columns=['SPY'])
            
            logger.info(f"Loaded {prices.shape[1]} assets over {prices.shape[0]} trading days.")
            return prices, benchmark
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise