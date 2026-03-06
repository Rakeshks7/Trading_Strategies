import logging
from utils.data_loader import DataLoader
from strategy.risk_manager import RiskManager
from strategy.execution_logic import ShortCallButterfly

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("MainHarness")

def main():
    logger.info("Initializing Short Call Butterfly Alpha Framework...")

    data_pipeline = DataLoader(ticker="SPY")
    risk_engine = RiskManager(account_size=100000.0) 
    strategy = ShortCallButterfly(risk_manager=risk_engine)

    spot_price, current_ivr = data_pipeline.get_underlying_metrics()
    logger.info(f"Market Data -> Spot: {spot_price}, IVR: {current_ivr}")
    
    options_chain = data_pipeline.fetch_live_chain(spot_price)
    logger.info(f"Ingested options chain with {len(options_chain)} strikes.")

    trade_order = strategy.generate_signal(spot_price, current_ivr, options_chain)

    if trade_order:
        logger.info("=== TRADE SIGNAL GENERATED ===")
        logger.info(f"Structure: Sell {trade_order['k1_short']}C / Buy 2x {trade_order['k2_long']}C / Sell {trade_order['k3_short']}C")
        logger.info(f"Net Credit per Spread: ${trade_order['net_credit']:.2f}")
        logger.info(f"Max Risk per Spread: ${trade_order['max_loss']:.2f}")
        logger.info(f"Position Size: {trade_order['contracts']} contracts")
        logger.info("==============================")
    else:
        logger.info("No valid trade criteria met today.")

if __name__ == "__main__":
    main()