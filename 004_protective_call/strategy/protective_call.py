import pandas as pd
from data.market_data import MarketDataHandler
from analytics.garch_volatility import GARCHForecaster
from analytics.option_pricing import BlackScholes
from risk.risk_manager import RiskManager
from config.settings import config

class ProtectiveCallStrategy:
    def __init__(self, ticker: str, account_value: float):
        self.ticker = ticker
        self.account = account_value
        self.data = MarketDataHandler()
        self.risk = RiskManager()
        
    def run_analysis(self):
        print(f"--- Analyzing {self.ticker} ---")

        df = self.data.get_historical_prices(self.ticker, config.LOOKBACK_PERIOD)
        current_price = df['close'].iloc[-1]

        garch = GARCHForecaster(df['returns'])
        forecast_vol = garch.forecast_volatility()
        print(f"GARCH Forecast Vol: {forecast_vol:.2%}")

        borrow_rate = self.data.get_borrow_rate(self.ticker)

        rolling_mean = df['close'].rolling(window=20).mean()
        rolling_std = df['close'].rolling(window=20).std()
        z_score = (current_price - rolling_mean.iloc[-1]) / rolling_std.iloc[-1]
        
        print(f"Current Z-Score: {z_score:.2f}")
        
        if z_score > config.Z_SCORE_ENTRY:
            print(">>> SHORT SIGNAL GENERATED (Overbought)")

            chain = self.data.get_option_chain(self.ticker, current_price)

            best_option = None
            min_delta_diff = 1.0
            
            for opt in chain:
                delta = BlackScholes.call_delta(current_price, opt.strike, 45/365, 0.05, forecast_vol)
                if abs(delta - config.TARGET_DELTA) < min_delta_diff:
                    min_delta_diff = abs(delta - config.TARGET_DELTA)
                    best_option = opt
            
            if best_option:
                if self.risk.validate_trade(borrow_rate, 50): 
                    shares = self.risk.calculate_position_size(self.account, current_price, forecast_vol)
                    self.execute_trade(shares, best_option)
                else:
                    print("Trade filtered by Risk Manager.")
        else:
            print("No Signal.")

    def execute_trade(self, shares, option):
        print(f"\n[EXECUTION] Sell Short {shares} shares of {self.ticker}")
        print(f"[EXECUTION] Buy {int(shares/100)+1} Calls | Strike: {option.strike} | Exp: {option.expiration}")
        print("[STATUS] Protective Call Position Locked.\n")