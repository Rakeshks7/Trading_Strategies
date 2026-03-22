import yaml
import logging
import pandas as pd
from data.data_loader import DataLoader
from models.kalman_filter import DynamicHedgeRatio
from execution.position_manager import PositionManager
from execution.risk_manager import RiskManager

logging.basicConfig(level=logging.INFO, format='%(message)s')

def load_config(path: str = "config/settings.yaml") -> dict:
    with open(path, "r") as file:
        return yaml.safe_load(file)

def main():
    print("\n" + "="*50)
    print("🚀 INITIALIZING DYNAMIC CROSS-HEDGE ENGINE")
    print("="*50 + "\n")

    config = load_config()

    loader = DataLoader(config['assets']['spot_ticker'], config['assets']['futures_ticker'])
    spot_px, fut_px = loader.fetch_data(start_date="2022-01-01", end_date="2024-01-01")

    spot_rets = np.log(spot_px / spot_px.shift(1)).dropna()
    fut_rets = np.log(fut_px / fut_px.shift(1)).dropna()

    df = pd.concat([spot_rets, fut_rets, fut_px], axis=1, join='inner')
    df.columns = ['spot_ret', 'fut_ret', 'fut_px']

    kf = DynamicHedgeRatio(
        trans_cov=config['kalman_params']['trans_cov'],
        obs_cov=config['kalman_params']['obs_cov']
    )
    df['Dynamic_OHR'] = kf.calculate_ohr(df['spot_ret'], df['fut_ret'])

    pm = PositionManager(
        spot_position_value=config['capital']['spot_position_value'],
        futures_multiplier=config['capital']['futures_multiplier']
    )
    df['Required_Short_Contracts'] = pm.calculate_contracts(df['Dynamic_OHR'], df['fut_px'])

    rm = RiskManager(
        zscore_threshold=config['risk_limits']['max_basis_zscore'],
        window=config['risk_limits']['rolling_window']
    )
    df['Basis_ZScore'] = rm.track_basis_risk(df['spot_ret'], df['fut_ret'], df['Dynamic_OHR'])

    print("\n" + "-"*50)
    print("CURRENT HEDGE STATE (LATEST TRADING DAY):")
    print("-"*50)
    latest = df.iloc[-1]
    print(f"Date:                       {df.index[-1].date()}")
    print(f"Optimal Hedge Ratio (Beta): {latest['Dynamic_OHR']:.4f}")
    print(f"Short Contracts Required:   {latest['Required_Short_Contracts']} contracts")
    print(f"Current Basis Z-Score:      {latest['Basis_ZScore']:.2f}")
    
    if abs(latest['Basis_ZScore']) > config['risk_limits']['max_basis_zscore']:
        print("🚨 ACTION REQUIRED: Basis blowout detected. Unwind futures leg immediately.")
    else:
        print("✅ Status: Hedge is tracking within normal parameters.")

if __name__ == "__main__":
    main()