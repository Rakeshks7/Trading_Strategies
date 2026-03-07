import numpy as np
import pandas as pd
from config import StrategyConfig
from core.black_scholes import put_price
from core.vol_surface import VolatilitySurface
from signals.regime_filter import VolatilitySqueezeDetector
from portfolio.slippage_engine import SlippageModel
from portfolio.risk_manager import RiskManager

def run():
    print("Initializing Short Put Butterfly Engine...\n")
    cfg = StrategyConfig()

    print("--> Loading Market Data...")
    np.random.seed(42)
    days = 252
    returns = np.random.normal(0, 0.01, days)
    returns[-20:] = np.random.normal(0, 0.003, 20) 
    prices = 100 * np.exp(np.cumsum(returns))
    df = pd.Series(prices)
    current_price = df.iloc[-1]

    print("--> Running Volatility Regime Filter...")
    detector = VolatilitySqueezeDetector(cfg.lookback_window, cfg.squeeze_percentile_threshold)
    is_squeeze = detector.generate_signal(df)
    
    if not is_squeeze:
        print("    [ABORT] Market is not in a volatility squeeze. Standing aside.")
        return
    print("    [SIGNAL] Volatility Squeeze detected! Constructing Butterfly...")

    surface = VolatilitySurface(atm_vol=0.15)

    std_dev_dist = current_price * 0.15 * np.sqrt(cfg.target_dte) * cfg.wing_width_std
    
    K_otm = np.array([current_price - std_dev_dist]) 
    K_atm = np.array([current_price])                
    K_itm = np.array([current_price + std_dev_dist]) 

    iv_otm = surface.get_iv(current_price, K_otm)
    iv_atm = surface.get_iv(current_price, K_atm)
    iv_itm = surface.get_iv(current_price, K_itm)

    p_otm = put_price(current_price, K_otm, cfg.target_dte, cfg.risk_free_rate, iv_otm)
    p_atm = put_price(current_price, K_atm, cfg.target_dte, cfg.risk_free_rate, iv_atm)
    p_itm = put_price(current_price, K_itm, cfg.target_dte, cfg.risk_free_rate, iv_itm)

    print("--> Modeling Execution Slippage...")
    slip_model = SlippageModel()
    slip_otm = slip_model.estimate_slippage(current_price, K_otm)
    slip_atm = slip_model.estimate_slippage(current_price, K_atm)
    slip_itm = slip_model.estimate_slippage(current_price, K_itm) 

    raw_credit = p_otm[0] + p_itm[0] - (2 * p_atm[0])
    total_slippage = slip_otm[0] + slip_itm[0] + (2 * slip_atm[0])
    net_credit_realized = raw_credit - total_slippage
    
    if net_credit_realized <= 0:
        print("    [ABORT] Slippage destroyed the credit. Trade is Negative EV.")
        return

    print("--> Sizing Position...")
    strike_width = K_itm[0] - K_atm[0]
    max_loss = strike_width - net_credit_realized

    estimated_win_prob = 0.35 
    win_loss_ratio = net_credit_realized / max_loss
    
    risk_manager = RiskManager(cfg.account_size, cfg.kelly_fraction, cfg.max_portfolio_heat)
    contracts = risk_manager.calculate_position_size(estimated_win_prob, win_loss_ratio, max_loss)

    print("\n" + "="*40)
    print("TRADE EXECUTION SUMMARY")
    print("="*40)
    print(f"Underlying Price:  ${current_price:.2f}")
    print(f"Strikes:           {K_otm[0]:.0f} / {K_atm[0]:.0f} / {K_itm[0]:.0f}")
    print(f"Raw Credit:        ${raw_credit:.2f}")
    print(f"Total Slippage:    ${total_slippage:.2f} (Watch the ITM wing!)")
    print(f"Realized Credit:   ${net_credit_realized:.2f}")
    print(f"Max Loss per Fly:  ${max_loss:.2f}")
    print(f"Optimal Contracts: {contracts}")
    print("="*40)

if __name__ == "__main__":
    run()